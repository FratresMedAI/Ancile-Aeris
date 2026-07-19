from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="causal_xai", executable="causal_xai_node", name="causal_xai_node", output="screen")
    ])
