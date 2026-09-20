import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    package_share = get_package_share_directory('nybble_robot')
    params_file = os.path.join(package_share, 'config', 'robot_params.yaml')

    return LaunchDescription([
        Node(
            package='nybble_robot',
            executable='camera_node',
            name='camera_node',
            output='screen',
            parameters=[params_file],
        ),
        Node(
            package='nybble_robot',
            executable='ultrasonic_node',
            name='ultrasonic_node',
            output='screen',
            parameters=[params_file],
        ),
        Node(
            package='nybble_robot',
            executable='behavior_node',
            name='behavior_node',
            output='screen',
            parameters=[params_file],
        ),
    ])
