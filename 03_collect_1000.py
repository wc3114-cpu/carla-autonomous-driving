import carla
import random
import os
import math
import queue
import numpy as np

HOST = "172.24.208.1"
PORT = 2000

IMAGE_W = 800
IMAGE_H = 600
FOV = 90
NUM_FRAMES = 1000
MAX_DISTANCE = 50.0

BASE_DIR = os.path.expanduser("~/carla_project/data/week1_1000")
IMAGE_DIR = os.path.join(BASE_DIR, "images")
YOLO_DIR = os.path.join(BASE_DIR, "labels_yolo")
KITTI_DIR = os.path.join(BASE_DIR, "labels_kitti")

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(YOLO_DIR, exist_ok=True)
os.makedirs(KITTI_DIR, exist_ok=True)


def build_projection_matrix(w, h, fov):
    focal = w / (2.0 * math.tan(fov * math.pi / 360.0))

    K = np.identity(3)
    K[0, 0] = focal
    K[1, 1] = focal
    K[0, 2] = w / 2.0
    K[1, 2] = h / 2.0

    return K


def project_point(location, K, world_to_camera):
    point = np.array([
        location.x,
        location.y,
        location.z,
        1.0
    ])

    point_camera = np.dot(world_to_camera, point)

    # CARLA / UE4 coordinates -> camera coordinates
    point_camera = np.array([
        point_camera[1],
        -point_camera[2],
        point_camera[0]
    ])

    if point_camera[2] <= 0:
        return None

    point_img = np.dot(K, point_camera)

    point_img[0] /= point_img[2]
    point_img[1] /= point_img[2]

    return point_img[0], point_img[1]


client = carla.Client(HOST, PORT)
client.set_timeout(30.0)

world = client.get_world()
blueprints = world.get_blueprint_library()

original_settings = world.get_settings()

settings = world.get_settings()
settings.synchronous_mode = True
settings.fixed_delta_seconds = 0.05
world.apply_settings(settings)

traffic_manager = client.get_trafficmanager(8000)
traffic_manager.set_synchronous_mode(True)

actors_to_destroy = []

try:
    # -------------------------
    # Spawn ego vehicle
    # -------------------------
    vehicle_bp = random.choice(
        blueprints.filter("vehicle.*")
    )

    spawn_points = world.get_map().get_spawn_points()
    random.shuffle(spawn_points)

    ego_vehicle = None

    for spawn_point in spawn_points:
        ego_vehicle = world.try_spawn_actor(
            vehicle_bp,
            spawn_point
        )

        if ego_vehicle is not None:
            break

    if ego_vehicle is None:
        raise RuntimeError("Could not spawn ego vehicle.")

    actors_to_destroy.append(ego_vehicle)

    ego_vehicle.set_autopilot(True, 8000)

    print("Ego vehicle:", ego_vehicle.type_id)

    # -------------------------
    # Spawn NPC vehicles
    # -------------------------
    npc_count = 0

    for spawn_point in spawn_points:
        if npc_count >= 30:
            break

        bp = random.choice(
            blueprints.filter("vehicle.*")
        )

        npc = world.try_spawn_actor(
            bp,
            spawn_point
        )

        if npc is not None:
            npc.set_autopilot(True, 8000)
            actors_to_destroy.append(npc)
            npc_count += 1

    print("NPC vehicles:", npc_count)

    # -------------------------
    # RGB camera
    # -------------------------
    camera_bp = blueprints.find(
        "sensor.camera.rgb"
    )

    camera_bp.set_attribute(
        "image_size_x",
        str(IMAGE_W)
    )

    camera_bp.set_attribute(
        "image_size_y",
        str(IMAGE_H)
    )

    camera_bp.set_attribute(
        "fov",
        str(FOV)
    )

    camera_transform = carla.Transform(
        carla.Location(
            x=1.5,
            z=2.4
        )
    )

    camera = world.spawn_actor(
        camera_bp,
        camera_transform,
        attach_to=ego_vehicle
    )

    actors_to_destroy.append(camera)

    image_queue = queue.Queue()
    camera.listen(image_queue.put)

    K = build_projection_matrix(
        IMAGE_W,
        IMAGE_H,
        FOV
    )

    # Let simulation settle
    for _ in range(20):
        world.tick()

    # -------------------------
    # Collect frames
    # -------------------------
    saved_frames = 0

    while saved_frames < NUM_FRAMES:

        world.tick()

        image = image_queue.get(timeout=5.0)

        frame_id = saved_frames

        image_path = os.path.join(
            IMAGE_DIR,
            f"{frame_id:06d}.png"
        )

        yolo_path = os.path.join(
            YOLO_DIR,
            f"{frame_id:06d}.txt"
        )

        kitti_path = os.path.join(
            KITTI_DIR,
            f"{frame_id:06d}.txt"
        )

        image.save_to_disk(image_path)

        world_to_camera = np.array(
            camera.get_transform().get_inverse_matrix()
        )

        yolo_lines = []
        kitti_lines = []

        vehicles = world.get_actors().filter(
            "vehicle.*"
        )

        ego_location = ego_vehicle.get_location()
        ego_forward = ego_vehicle.get_transform().get_forward_vector()

        for actor in vehicles:

            if actor.id == ego_vehicle.id:
                continue

            distance = actor.get_location().distance(
                ego_location
            )

            if distance > MAX_DISTANCE:
                continue

            ray = actor.get_location() - ego_location

            if ego_forward.dot(ray) <= 0:
                continue

            bbox = actor.bounding_box

            vertices = bbox.get_world_vertices(
                actor.get_transform()
            )

            projected = []

            for vertex in vertices:

                point = project_point(
                    vertex,
                    K,
                    world_to_camera
                )

                if point is not None:
                    projected.append(point)

            if len(projected) < 4:
                continue

            xs = [p[0] for p in projected]
            ys = [p[1] for p in projected]

            x_min = max(0, min(xs))
            x_max = min(IMAGE_W - 1, max(xs))

            y_min = max(0, min(ys))
            y_max = min(IMAGE_H - 1, max(ys))

            if x_max <= x_min or y_max <= y_min:
                continue

            box_width = x_max - x_min
            box_height = y_max - y_min

            # Ignore tiny boxes
            if box_width < 8 or box_height < 8:
                continue

            # -------------------------
            # YOLO format
            # class 0 = vehicle
            # -------------------------
            x_center = (
                (x_min + x_max) / 2.0
            ) / IMAGE_W

            y_center = (
                (y_min + y_max) / 2.0
            ) / IMAGE_H

            norm_width = box_width / IMAGE_W
            norm_height = box_height / IMAGE_H

            yolo_lines.append(
                f"0 "
                f"{x_center:.6f} "
                f"{y_center:.6f} "
                f"{norm_width:.6f} "
                f"{norm_height:.6f}"
            )

            # -------------------------
            # KITTI-style 2D label
            # -------------------------
            kitti_lines.append(
                "Car "
                "0 0 -10 "
                f"{x_min:.2f} "
                f"{y_min:.2f} "
                f"{x_max:.2f} "
                f"{y_max:.2f} "
                "-1 -1 -1 "
                "-1000 -1000 -1000 "
                "-10"
            )

        with open(
            yolo_path,
            "w"
        ) as f:

            f.write(
                "\n".join(yolo_lines)
            )

        with open(
            kitti_path,
            "w"
        ) as f:

            f.write(
                "\n".join(kitti_lines)
            )

        saved_frames += 1

        print(
            f"Saved "
            f"{saved_frames}/"
            f"{NUM_FRAMES} "
            f"| labels: "
            f"{len(yolo_lines)}"
        )

finally:

    try:
        camera.stop()
    except Exception:
        pass

    for actor in reversed(
        actors_to_destroy
    ):

        try:
            actor.destroy()
        except Exception:
            pass

    traffic_manager.set_synchronous_mode(
        False
    )

    world.apply_settings(
        original_settings
    )

    print("Collection finished.")
