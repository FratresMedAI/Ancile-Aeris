from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package="ancile_aeris_safety_gate",
            executable="ancile_aeris_safety_gate_node",
            name="ancile_aeris_safety_gate_node",
            output="screen",
        ),
    ])
