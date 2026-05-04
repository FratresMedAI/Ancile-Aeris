from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package="blacksky_core",
            executable="blacksky_core_node",
            name="blacksky_core_node",
            output="screen",
        )
    ])
