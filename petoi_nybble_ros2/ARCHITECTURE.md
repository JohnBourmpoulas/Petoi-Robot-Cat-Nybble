# Architecture

```text
USB Camera
    |
    v
camera_node ---- /detected_person ----+
                                      |
                                      v
                                behavior_node ---- /robot_command ---> future motor node
                                      ^
                                      |
ultrasonic_node ---- /distance_cm ----+
    ^
    |
HC-SR04
```

## Nodes

### `camera_node`
Reads a USB camera, performs face recognition, and publishes a name on `/detected_person`.

### `ultrasonic_node`
Reads an HC-SR04-style sensor using Raspberry Pi BCM GPIO and publishes centimeters on `/distance_cm`.

### `behavior_node`
Subscribes to both sensor topics and publishes a simple high-level decision on `/robot_command`.
Obstacle stopping has priority over face behavior.

## Why split it into nodes?

Each node has one responsibility. The behavior code does not need to know how OpenCV or GPIO works; it only consumes ROS messages. This makes individual components easier to replace, test, and extend.
