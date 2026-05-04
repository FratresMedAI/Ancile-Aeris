from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="copilot", executable="copilot_node", name="copilot_node", output="screen")
    ])
