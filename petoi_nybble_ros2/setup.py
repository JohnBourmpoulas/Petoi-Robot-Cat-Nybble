from glob import glob
import os

from setuptools import find_packages, setup

package_name = 'nybble_robot'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'known_faces'), glob('known_faces/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='John Bourmpoulas',
    maintainer_email='student@example.com',  # Replace with your preferred public email.
    description='ROS 2 Jazzy rewrite of a Petoi Nybble vision and ultrasonic behavior project.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera_node = nybble_robot.camera_node:main',
            'ultrasonic_node = nybble_robot.ultrasonic_node:main',
            'behavior_node = nybble_robot.behavior_node:main',
        ],
    },
)
