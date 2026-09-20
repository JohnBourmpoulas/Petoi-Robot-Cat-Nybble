# Petoi Nybble ROS 2

A ROS 2 Jazzy rewrite of my first robotics-lab project based on the Petoi Nybble robot. The original project used Python, a USB camera with face recognition, and an ultrasonic distance sensor. This repository reorganizes that functionality into independent ROS 2 nodes so the sensor and behavior components communicate through topics and can be launched as one system.

> This repository covers the camera, ultrasonic sensing, and behavior/decision layer. It does **not** implement the original Nybble locomotion protocol. `/robot_command` is intentionally the interface for a future movement/controller node.

## Architecture

```text
USB Camera
    |
    v
camera_node ---- /detected_person ----+
                                      |
                                      v
                                behavior_node ---- /robot_command
                                      ^
                                      |
ultrasonic_node ---- /distance_cm ----+
    ^
    |
HC-SR04
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for a more detailed explanation.

## ROS 2 interfaces

| Node | Publishes | Subscribes | Main parameters |
|---|---|---|---|
| `camera_node` | `/detected_person` (`std_msgs/String`) | — | `camera_index`, `face_match_tolerance`, `frame_period_sec` |
| `ultrasonic_node` | `/distance_cm` (`std_msgs/Float32`) | — | `trigger_pin`, `echo_pin`, `measurement_period_sec` |
| `behavior_node` | `/robot_command` (`std_msgs/String`) | `/detected_person`, `/distance_cm` | `stop_distance_cm` |

Possible `/robot_command` values are `IDLE`, `STOP_OBSTACLE`, `UNKNOWN_PERSON`, and `OWNER_SEEN:<name>`.

## Repository structure

```text
petoi_nybble_ros2/
├── nybble_robot/
│   ├── camera_node.py
│   ├── ultrasonic_node.py
│   └── behavior_node.py
├── launch/
│   └── robot.launch.py
├── config/
│   └── robot_params.yaml
├── known_faces/
├── resource/
├── test/
├── package.xml
├── setup.py
├── setup.cfg
├── requirements.txt
├── ARCHITECTURE.md
├── LICENSE
└── README.md
```

This follows the normal ROS 2 `ament_python` package layout: Python modules in the package directory, launch files in `launch/`, configuration in `config/`, package metadata in `package.xml`/`setup.py`, plus repository documentation and a license.

## Hardware

- Raspberry Pi (original project / intended hardware target)
- USB camera
- HC-SR04-style ultrasonic sensor

### Important HC-SR04 wiring note

A classic HC-SR04 ECHO pin outputs about 5 V while Raspberry Pi GPIO is 3.3 V logic. Use an appropriate voltage divider or level shifter on ECHO before connecting it to the Pi GPIO.

Default BCM GPIO values in `config/robot_params.yaml`:

```text
TRIG -> GPIO 23
ECHO -> GPIO 24   (through safe level conversion)
```

## Software

Target environment:

- Ubuntu 24.04
- ROS 2 Jazzy
- Python 3
- OpenCV
- `face_recognition`
- `RPi.GPIO` on Raspberry Pi

## Installation

Clone this repository into the `src` directory of a ROS 2 workspace:

```bash
git clone <your-repository-url> ~/ros2_ws/src/nybble_robot
cd ~/ros2_ws
```

Install ROS dependencies:

```bash
rosdep install --from-paths src --ignore-src -r -y
```

Install the non-ROS Python face-recognition dependency in the environment where the node will run:

```bash
python3 -m pip install face_recognition
```

Then build and source the workspace:

```bash
colcon build --symlink-install --packages-select nybble_robot
source install/setup.bash
```

## Known faces

Put one image per person in `known_faces/`. The filename becomes the person's name:

```text
known_faces/
├── John.jpg
└── Alice.jpg
```

For a public GitHub repository, consider keeping personal face photos out of Git and adding the image extensions in `.gitignore`.

After adding/changing images, rebuild so they are copied into the package share directory:

```bash
colcon build --symlink-install --packages-select nybble_robot
source install/setup.bash
```

## Run the whole robot stack

```bash
ros2 launch nybble_robot robot.launch.py
```

Or run nodes individually:

```bash
ros2 run nybble_robot camera_node
ros2 run nybble_robot ultrasonic_node
ros2 run nybble_robot behavior_node
```

## Inspect the ROS graph

In another sourced terminal:

```bash
ros2 node list
ros2 topic list
ros2 topic echo /detected_person
ros2 topic echo /distance_cm
ros2 topic echo /robot_command
```

## Configuration

Edit `config/robot_params.yaml` to change hardware and behavior settings without editing the node source code:

```yaml
ultrasonic_node:
  ros__parameters:
    trigger_pin: 23
    echo_pin: 24

behavior_node:
  ros__parameters:
    stop_distance_cm: 25.0
```

## Development on a Mac / Docker

The ROS architecture and `behavior_node` can be developed in a ROS 2 Jazzy container on Apple Silicon. The hardware-specific parts have limitations:

- `ultrasonic_node` requires Raspberry Pi GPIO and should run on the Pi.
- USB camera access must be explicitly passed through to a Linux container; macOS Docker does not expose `/dev/video0` in the same way as native Linux.

For real hardware testing, the Raspberry Pi is the intended runtime target.

## Next steps

Natural extensions are a motor/controller node, proper custom ROS messages, camera image topics (`sensor_msgs/Image`), diagnostics, simulation, and eventually a wheeled ROS 2 platform using odometry, TF, SLAM, and Nav2.

## License

MIT. See [LICENSE](LICENSE).
