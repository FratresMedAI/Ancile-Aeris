from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="fusion_node", executable="fusion_node", name="fusion_node", output="screen"),
    ])
