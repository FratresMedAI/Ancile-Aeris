from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package="ancile_aeris_sensor_resilience",
            executable="ancile_aeris_sensor_resilience_node",
            name="ancile_aeris_sensor_resilience_node",
            output="screen",
            prefix="python3",
        ),
    ])
