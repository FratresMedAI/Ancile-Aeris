from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="ew_node", executable="ew_node", name="ew_node", output="screen"),
    ])
