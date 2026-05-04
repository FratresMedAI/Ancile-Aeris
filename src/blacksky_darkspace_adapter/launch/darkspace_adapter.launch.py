from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package="blacksky_darkspace_adapter",
            executable="darkspace_adapter_node",
            name="darkspace_adapter_node",
            output="screen",
            parameters=["/opt/counterdrone_ws/src/blacksky_darkspace_adapter/config/darkspace_adapter.yaml"],
        )
    ])
