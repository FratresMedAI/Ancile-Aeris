from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package="blacksky_sensor",
            executable="blacksky_fusion_node",
            name="blacksky_fusion_node",
            output="screen",
        )
    ])
