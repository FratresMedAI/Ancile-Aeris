from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package="video_analytics_node",
            executable="video_analytics_node",
            name="video_analytics_node",
            output="screen",
        ),
    ])
