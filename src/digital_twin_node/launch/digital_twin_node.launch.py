from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="digital_twin_node", executable="digital_twin_node", name="digital_twin_node", output="screen"),
    ])
