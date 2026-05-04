from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package="blacksky_digital_twin",
            executable="digital_twin_node",
            name="blacksky_digital_twin_node",
            output="screen",
        )
    ])
