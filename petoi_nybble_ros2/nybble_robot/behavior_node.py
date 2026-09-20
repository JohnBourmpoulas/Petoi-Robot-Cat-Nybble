import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String


class BehaviorNode(Node):
    """Combine face and distance data into a simple high-level robot command."""

    def __init__(self):
        super().__init__('behavior_node')

        self.declare_parameter('stop_distance_cm', 25.0)
        self.stop_distance_cm = float(self.get_parameter('stop_distance_cm').value)

        self.last_person = 'Nobody'
        self.last_distance = None
        self.last_command = None

        self.create_subscription(String, '/detected_person', self._person_callback, 10)
        self.create_subscription(Float32, '/distance_cm', self._distance_callback, 10)
        self.command_publisher = self.create_publisher(String, '/robot_command', 10)

    def _person_callback(self, msg):
        self.last_person = msg.data
        self._decide()

    def _distance_callback(self, msg):
        self.last_distance = float(msg.data)
        self._decide()

    def _decide(self):
        command = 'IDLE'

        if self.last_distance is not None and self.last_distance < self.stop_distance_cm:
            command = 'STOP_OBSTACLE'
        elif self.last_person not in ('Nobody', 'Unknown'):
            command = f'OWNER_SEEN:{self.last_person}'
        elif self.last_person == 'Unknown':
            command = 'UNKNOWN_PERSON'

        msg = String()
        msg.data = command
        self.command_publisher.publish(msg)

        if command != self.last_command:
            self.get_logger().info(
                f'person={self.last_person}, distance={self.last_distance}, command={command}'
            )
            self.last_command = command


def main(args=None):
    rclpy.init(args=args)
    node = BehaviorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
