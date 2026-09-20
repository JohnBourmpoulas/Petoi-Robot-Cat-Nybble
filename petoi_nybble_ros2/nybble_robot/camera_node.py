import os

import cv2
import face_recognition
import rclpy
from ament_index_python.packages import get_package_share_directory
from rclpy.node import Node
from std_msgs.msg import String


class CameraNode(Node):
    """Detect faces from a USB camera and publish the best recognized person."""

    def __init__(self):
        super().__init__('camera_node')

        self.declare_parameter('camera_index', 0)
        self.declare_parameter('face_match_tolerance', 0.6)
        self.declare_parameter('frame_period_sec', 0.1)

        camera_index = int(self.get_parameter('camera_index').value)
        self.tolerance = float(self.get_parameter('face_match_tolerance').value)
        frame_period = float(self.get_parameter('frame_period_sec').value)

        self.publisher = self.create_publisher(String, '/detected_person', 10)

        known_faces_dir = os.path.join(
            get_package_share_directory('nybble_robot'), 'known_faces'
        )
        self.people = self._load_known_faces(known_faces_dir)

        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_V4L2)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

        if not self.cap.isOpened():
            self.get_logger().error(f'Could not open camera index {camera_index}.')

        self.timer = self.create_timer(frame_period, self._process_frame)

    def _load_known_faces(self, folder):
        people = []
        if not os.path.isdir(folder):
            self.get_logger().warning(f'Known-faces directory not found: {folder}')
            return people

        for filename in sorted(os.listdir(folder)):
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue

            path = os.path.join(folder, filename)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)

            if not encodings:
                self.get_logger().warning(f'No face found in {filename}; skipping it.')
                continue

            people.append({
                'name': os.path.splitext(filename)[0],
                'encoding': encodings[0],
            })

        self.get_logger().info(f'Loaded {len(people)} known face(s).')
        return people

    def _recognize(self, encoding):
        if not self.people:
            return 'Unknown'

        known_encodings = [person['encoding'] for person in self.people]
        distances = face_recognition.face_distance(known_encodings, encoding)
        best_index = int(distances.argmin())

        if float(distances[best_index]) <= self.tolerance:
            return self.people[best_index]['name']
        return 'Unknown'

    def _process_frame(self):
        if not self.cap.isOpened():
            return

        ok, frame = self.cap.read()
        if not ok:
            self.get_logger().warning('Could not read a frame from the camera.')
            return

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, locations)
        names = [self._recognize(encoding) for encoding in encodings]

        msg = String()
        msg.data = names[0] if names else 'Nobody'
        self.publisher.publish(msg)

    def destroy_node(self):
        if self.cap is not None:
            self.cap.release()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = CameraNode()
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
