from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package="clearsky_os_operator_copilot",
            executable="clearsky_os_operator_copilot_node",
            name="clearsky_os_operator_copilot_node",
            output="screen",
            prefix="python3",
        ),
    ])
