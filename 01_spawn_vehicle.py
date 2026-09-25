import carla
import random
import time

HOST = "172.24.208.1"
PORT = 2000

client = carla.Client(HOST, PORT)
client.set_timeout(10.0)

world = client.get_world()
blueprint_library = world.get_blueprint_library()

# Choose a random vehicle
vehicle_blueprints = blueprint_library.filter("vehicle.*")
vehicle_bp = random.choice(vehicle_blueprints)

# Try different spawn points until a vehicle is successfully created
spawn_points = world.get_map().get_spawn_points()
random.shuffle(spawn_points)

vehicle = None

for spawn_point in spawn_points:
    vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)
    if vehicle is not None:
        break

if vehicle is None:
    raise RuntimeError("Failed to spawn vehicle")

print("Vehicle spawned:", vehicle.type_id)

# Enable autopilot
vehicle.set_autopilot(True)
print("Autopilot enabled")

spectator = world.get_spectator()

try:
    # Run for 30 seconds
    for _ in range(300):
        transform = vehicle.get_transform()

        # Chase camera behind the vehicle
        camera_transform = carla.Transform(
            transform.transform(carla.Location(x=-8, z=4)),
            transform.rotation
        )

        spectator.set_transform(camera_transform)

        time.sleep(0.1)

finally:
    vehicle.destroy()
    print("Vehicle destroyed")
