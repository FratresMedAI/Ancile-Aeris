from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package="ancile_aeris_fusion",
            executable="ancile_aeris_fusion_node",
            name="ancile_aeris_fusion_node",
            output="screen",
            prefix="python3",
        )
    ])
