from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package="clearsky_os_sensor_resilience",
            executable="clearsky_os_sensor_resilience_node",
            name="clearsky_os_sensor_resilience_node",
            output="screen",
            prefix="python3",
        ),
    ])
