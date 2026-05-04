from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="cyber_node", executable="cyber_node", name="cyber_node", output="screen"),
    ])
