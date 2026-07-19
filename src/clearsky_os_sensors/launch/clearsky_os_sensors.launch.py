from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package="clearsky_os_sensors",
            executable="clearsky_os_visual_node",
            name="clearsky_os_visual_node",
            output="screen",
            prefix="python3",
        ),
        Node(
            package="clearsky_os_sensors",
            executable="clearsky_os_thermal_node",
            name="clearsky_os_thermal_node",
            output="screen",
            prefix="python3",
        ),
        Node(
            package="clearsky_os_sensors",
            executable="clearsky_os_acoustic_node",
            name="clearsky_os_acoustic_node",
            output="screen",
            prefix="python3",
        ),
        Node(
            package="clearsky_os_sensors",
            executable="clearsky_os_rf_node",
            name="clearsky_os_rf_node",
            output="screen",
            prefix="python3",
        ),
        Node(
            package="clearsky_os_sensors",
            executable="clearsky_os_demo_context_node",
            name="clearsky_os_demo_context_node",
            output="screen",
            prefix="python3",
        ),
    ])
