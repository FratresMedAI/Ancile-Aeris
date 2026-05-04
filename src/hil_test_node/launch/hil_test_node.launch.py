from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="hil_test_node", executable="hil_test_node", name="hil_test_node", output="screen"),
    ])
