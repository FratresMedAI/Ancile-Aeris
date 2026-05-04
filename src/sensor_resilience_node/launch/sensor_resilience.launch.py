from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package="sensor_resilience_node",
            executable="sensor_resilience_node",
            name="sensor_resilience_node",
            output="screen",
        ),
    ])
