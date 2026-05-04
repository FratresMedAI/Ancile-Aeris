from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package="blacksky_hmi",
            executable="human_interface_node",
            name="human_interface_node",
            output="screen",
        )
    ])
