from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="cognitive_ew", executable="cognitive_ew_node", name="cognitive_ew_node", output="screen")
    ])
