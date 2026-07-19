from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package="clearsky_os_safety_gate",
            executable="clearsky_os_safety_gate_node",
            name="clearsky_os_safety_gate_node",
            output="screen",
            prefix="python3",
        ),
    ])
