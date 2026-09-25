import carla
import random
import os
import threading

HOST = "172.24.208.1"
PORT = 2000
NUM_IMAGES = 100

client = carla.Client(HOST, PORT)
client.set_timeout(30.0)

world = client.get_world()
blueprints = world.get_blueprint_library()

# Spawn a vehicle
vehicle_bp = blueprints.filter("vehicle.*")[0]
spawn_points = world.get_map().get_spawn_points()
random.shuffle(spawn_points)

vehicle = None
for point in spawn_points:
    vehicle = world.try_spawn_actor(vehicle_bp, point)
    if vehicle is not None:
        break

if vehicle is None:
    raise RuntimeError("Failed to spawn vehicle")

vehicle.set_autopilot(True)
print("Vehicle spawned:", vehicle.type_id)

# Configure RGB camera
camera_bp = blueprints.find("sensor.camera.rgb")
camera_bp.set_attribute("image_size_x", "800")
camera_bp.set_attribute("image_size_y", "600")
camera_bp.set_attribute("fov", "90")
camera_bp.set_attribute("sensor_tick", "0.1")

camera_transform = carla.Transform(
    carla.Location(x=1.5, z=2.4)
)

camera = world.spawn_actor(
    camera_bp,
    camera_transform,
    attach_to=vehicle
)

output_dir = os.path.expanduser("~/carla_project/data/rgb")
os.makedirs(output_dir, exist_ok=True)

count = 0
finished = threading.Event()

def save_image(image):
    global count

    if count < NUM_IMAGES:
        filename = os.path.join(
            output_dir,
            f"{count:06d}.png"
        )

        image.save_to_disk(filename)
        count += 1

        print(f"Saved {count}/{NUM_IMAGES}")

    if count >= NUM_IMAGES:
        finished.set()

camera.listen(save_image)

try:
    finished.wait(timeout=60)

finally:
    camera.stop()
    camera.destroy()
    vehicle.destroy()

print("Data collection finished.")
print("Images saved to:", output_dir)
