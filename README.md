# Petoi Robot Cat Nybble — Original Project & ROS 2 Rewrite

A robotics project based on the **Petoi Nybble robotic cat**, originally developed as my first hands-on robotics project using a Raspberry Pi, Python, computer vision, and ultrasonic sensing.

The project was later revisited and redesigned using **ROS 2 Jazzy**, with the goal of converting the original implementation into a modular ROS 2 architecture based on independent nodes, topics, parameters, and launch files.

This repository therefore contains both the **original implementation** and its **ROS 2 rewrite**, showing the evolution of the project from a simple Python-based robotics application to a more structured robotic software architecture.

---

## Project Evolution

```text
Original Python Project
        │
        │ Raspberry Pi + Sensors
        │
        ▼
Camera + Face Recognition
Ultrasonic Distance Sensing
Robot Behavior Logic
        │
        │
        ▼
   ROS 2 Rewrite
        │
        ├── camera_node
        ├── ultrasonic_node
        └── behavior_node
              │
              ▼
     ROS 2 Topics / Parameters
          / Launch System
```

---

# 1. Original Project

The original version of this project was developed during a robotics class and was my first practical implementation combining **Python software with physical robotic hardware**.

The goal was to experiment with how a robot could perceive its environment using a camera and an ultrasonic sensor.

The original source code can be found in:

```text
cat_project/
```

### Main Features

The original implementation included:

- Raspberry Pi as the main computer
- USB camera
- Computer vision using OpenCV
- Face detection and recognition
- Recognition of a known person / robot owner
- Ultrasonic distance measurement
- Basic robot behavior logic
- Python-based hardware interaction

### Face Recognition

The camera module captures images from a USB camera and processes them using:

- `OpenCV`
- `face_recognition`

Known face images are loaded and encoded so that faces detected by the camera can be compared against them.

The objective was to allow the robot to distinguish its owner from an unknown person.

### Ultrasonic Sensing

An ultrasonic distance sensor is used to measure the distance between the robot and nearby objects.

This information can be used by the robot behavior logic to detect obstacles and react when an object is too close.

### Original Architecture

The original implementation follows a relatively simple Python architecture where the different hardware and behavior components are directly connected through the application code.

```text
           Raspberry Pi
                │
       ┌────────┴────────┐
       │                 │
       ▼                 ▼
  USB Camera       Ultrasonic Sensor
       │                 │
       ▼                 ▼
Face Recognition    Distance Reading
       │                 │
       └────────┬────────┘
                ▼
          Robot Behavior
```

This implementation was intentionally simple and served as an introduction to robotics, sensors, computer vision, and hardware/software integration.

---

# 2. ROS 2 Jazzy Rewrite

The project was later revisited while learning **ROS 2**.

Instead of keeping the camera, ultrasonic sensor, and robot behavior tightly coupled inside the same application, the system was redesigned into **independent ROS 2 nodes**.

The ROS 2 implementation can be found in:

```text
petoi_nybble_ros2/
```

The rewrite targets:

- **ROS 2 Jazzy**
- **Python / rclpy**
- **Ubuntu 24.04**
- **Raspberry Pi / Linux**

---

## ROS 2 Architecture

The ROS 2 version currently contains three main nodes:

### `camera_node`

Responsible for:

- Accessing the USB camera
- Capturing frames using OpenCV
- Detecting faces
- Comparing detected faces with known face encodings
- Publishing the detected person's name

Publishes:

```text
/detected_person
```

Message type:

```text
std_msgs/String
```

---

### `ultrasonic_node`

Responsible for:

- Controlling the ultrasonic sensor GPIO pins
- Triggering distance measurements
- Calculating the measured distance
- Publishing distance information

Publishes:

```text
/distance_cm
```

Message type:

```text
std_msgs/Float32
```

The GPIO pins are configurable using ROS 2 parameters.

---

### `behavior_node`

The behavior node combines information coming from the other nodes.

It subscribes to:

```text
/detected_person
/distance_cm
```

and uses this information to determine the current robot behavior.

For example:

```text
Distance < stop_distance
        ↓
STOP_OBSTACLE
```

or:

```text
Known person detected
        ↓
OWNER_SEEN
```

The resulting command is published to:

```text
/robot_command
```

---

## Node Communication

```text
USB Camera
    │
    ▼
camera_node
    │
    │ /detected_person
    │
    └──────────────────┐
                       │
                       ▼
                 behavior_node
                       │
                       │ /robot_command
                       ▼
               Future Motor /
               Movement Node
                       ▲
                       │
    ┌──────────────────┘
    │ /distance_cm
    │
ultrasonic_node
    ▲
    │
Ultrasonic Sensor
```

One of the main advantages of this architecture is that each component has a **single responsibility**.

For example, the behavior node does not need to know how the camera works or how the ultrasonic distance is calculated. It only consumes the information published by those nodes.

---

## ROS 2 Parameters

Hardware-specific and behavioral settings are exposed as ROS 2 parameters.

For example:

```yaml
ultrasonic_node:
  ros__parameters:
    trigger_pin: 23
    echo_pin: 24

behavior_node:
  ros__parameters:
    stop_distance_cm: 25.0
```

This allows hardware connections and behavior thresholds to be changed without modifying the main node logic.

The configuration is stored in:

```text
petoi_nybble_ros2/config/robot_params.yaml
```

---

## ROS 2 Launch System

Instead of manually starting every node separately, the project includes a ROS 2 launch file:

```text
petoi_nybble_ros2/launch/robot.launch.py
```

The launch file starts:

```text
camera_node
ultrasonic_node
behavior_node
```

together with their configuration.

The complete system can therefore be started using:

```bash
ros2 launch nybble_robot robot.launch.py
```

---

# Repository Structure

```text
Petoi-Robot-Cat-Nybble/
│
├── cat_project/
│   ├── camera.py
│   ├── ultraSonic.py
│   └── RobotCat.py
│
├── petoi_nybble_ros2/
│   ├── nybble_robot/
│   │   ├── camera_node.py
│   │   ├── ultrasonic_node.py
│   │   └── behavior_node.py
│   │
│   ├── launch/
│   │   └── robot.launch.py
│   │
│   ├── config/
│   │   └── robot_params.yaml
│   │
│   ├── known_faces/
│   ├── resource/
│   ├── test/
│   │
│   ├── package.xml
│   ├── setup.py
│   ├── setup.cfg
│   ├── requirements.txt
│   ├── ARCHITECTURE.md
│   └── README.md
│
└── README.md
```

---

# Original vs ROS 2 Version

| Original Project | ROS 2 Rewrite |
|---|---|
| Python application | ROS 2 Python package |
| Direct component interaction | ROS 2 node communication |
| Camera code | `camera_node` |
| Ultrasonic code | `ultrasonic_node` |
| Behavior logic | `behavior_node` |
| Values configured in application | ROS 2 parameters |
| Components started manually | ROS 2 launch system |
| Tightly connected components | Modular node architecture |

The ROS 2 rewrite is not intended to replace the history of the original project. Instead, it demonstrates how the same robotic functionality can be reorganized using ROS 2 concepts.

---

# Technologies

### Original Project

- Python
- Raspberry Pi
- OpenCV
- face_recognition
- USB Camera
- Ultrasonic Sensor
- GPIO

### ROS 2 Rewrite

- ROS 2 Jazzy
- Python
- rclpy
- ROS 2 Topics
- ROS 2 Parameters
- ROS 2 Launch
- std_msgs
- OpenCV
- face_recognition

---

# Current Status

The original project was an educational prototype and was not developed into a complete autonomous robot.

The ROS 2 rewrite currently focuses on restructuring the original sensing and behavior functionality into a modular ROS 2 architecture.

The current implementation demonstrates:

- Camera integration
- Face recognition
- Ultrasonic sensing
- Inter-node communication
- ROS 2 parameters
- ROS 2 launch files
- Basic robot behavior coordination

Motor control and full locomotion are not currently implemented in the ROS 2 version.

A future extension could introduce a dedicated movement node:

```text
behavior_node
      │
      │ /robot_command
      ▼
  motor_node
      │
      ▼
Robot Movement
```

This would keep the movement hardware independent from the perception and decision-making nodes.

---

# What I Learned

The original project provided practical experience with:

- Python robotics programming
- Raspberry Pi GPIO
- Camera integration
- Computer vision
- Face recognition
- Ultrasonic sensors
- Hardware/software integration

Revisiting the project with ROS 2 provided an opportunity to redesign the same system around:

- Modular robot software architecture
- Independent ROS 2 nodes
- Publisher/subscriber communication
- ROS 2 topics and messages
- Parameters
- Launch files
- Package organization
- Separation of sensing, decision-making, and actuation

This repository therefore also documents the evolution of the project and the transition from a simple Python robotics application to a ROS 2-based architecture.

---

## License

This project is provided for educational and robotics experimentation purposes.
