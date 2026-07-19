from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="hyperspectral_stub", executable="hyperspectral_stub_node", name="hyperspectral_stub_node", output="screen")
    ])
