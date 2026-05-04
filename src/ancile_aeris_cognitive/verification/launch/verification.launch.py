from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="verification", executable="verification_node", name="verification_node", output="screen")
    ])
