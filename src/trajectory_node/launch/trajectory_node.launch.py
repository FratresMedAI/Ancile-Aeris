from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="trajectory_node", executable="trajectory_node", name="trajectory_node", output="screen"),
    ])
