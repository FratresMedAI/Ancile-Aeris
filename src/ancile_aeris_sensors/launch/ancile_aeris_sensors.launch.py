from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package="ancile_aeris_sensors",
            executable="ancile_aeris_visual_node",
            name="ancile_aeris_visual_node",
            output="screen",
            prefix="python3",
        ),
        Node(
            package="ancile_aeris_sensors",
            executable="ancile_aeris_thermal_node",
            name="ancile_aeris_thermal_node",
            output="screen",
            prefix="python3",
        ),
        Node(
            package="ancile_aeris_sensors",
            executable="ancile_aeris_acoustic_node",
            name="ancile_aeris_acoustic_node",
            output="screen",
            prefix="python3",
        ),
        Node(
            package="ancile_aeris_sensors",
            executable="ancile_aeris_rf_node",
            name="ancile_aeris_rf_node",
            output="screen",
            prefix="python3",
        ),
        Node(
            package="ancile_aeris_sensors",
            executable="ancile_aeris_demo_context_node",
            name="ancile_aeris_demo_context_node",
            output="screen",
            prefix="python3",
        ),
    ])
