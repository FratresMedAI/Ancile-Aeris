from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="video_analytics", executable="video_analytics_node", name="video_analytics_node_v2", output="screen")
    ])
