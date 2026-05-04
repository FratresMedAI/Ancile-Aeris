from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package="operator_copilot_node",
            executable="operator_copilot_node",
            name="operator_copilot_node",
            output="screen",
        ),
    ])
