from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package="ancile_aeris_operator_copilot",
            executable="ancile_aeris_operator_copilot_node",
            name="ancile_aeris_operator_copilot_node",
            output="screen",
        ),
    ])
