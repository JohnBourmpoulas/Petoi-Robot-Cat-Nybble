import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

try:
    import RPi.GPIO as GPIO
except ImportError:
    GPIO = None


class UltrasonicNode(Node):
    """Read an HC-SR04-style ultrasonic sensor and publish distance in cm."""

    def __init__(self):
        super().__init__('ultrasonic_node')

        self.declare_parameter('trigger_pin', 23)
        self.declare_parameter('echo_pin', 24)
        self.declare_parameter('measurement_period_sec', 0.2)

        self.trigger_pin = int(self.get_parameter('trigger_pin').value)
        self.echo_pin = int(self.get_parameter('echo_pin').value)
        period = float(self.get_parameter('measurement_period_sec').value)

        self.publisher = self.create_publisher(Float32, '/distance_cm', 10)
        self.gpio_ready = False

        if GPIO is None:
            self.get_logger().error(
                'RPi.GPIO is unavailable. Run this node on a Raspberry Pi with GPIO access.'
            )
            return

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.output(self.trigger_pin, False)
        self.gpio_ready = True
        time.sleep(0.05)

        self.timer = self.create_timer(period, self._measure_and_publish)

    def _read_distance_cm(self):
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)

        deadline = time.monotonic() + 0.03
        while GPIO.input(self.echo_pin) == 0:
            if time.monotonic() > deadline:
                return None
        pulse_start = time.monotonic()

        deadline = time.monotonic() + 0.03
        while GPIO.input(self.echo_pin) == 1:
            if time.monotonic() > deadline:
                return None
        pulse_end = time.monotonic()

        return ((pulse_end - pulse_start) * 34300.0) / 2.0

    def _measure_and_publish(self):
        distance = self._read_distance_cm()
        if distance is None:
            self.get_logger().warning('Ultrasonic measurement timed out.')
            return

        msg = Float32()
        msg.data = float(distance)
        self.publisher.publish(msg)

    def destroy_node(self):
        if GPIO is not None and self.gpio_ready:
            GPIO.cleanup()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = UltrasonicNode()
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
