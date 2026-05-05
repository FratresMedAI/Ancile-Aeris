from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="scout_mothership", executable="scout_mothership_node", name="scout_mothership_node", output="screen")
    ])
