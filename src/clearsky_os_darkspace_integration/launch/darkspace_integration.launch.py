from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription(
        [
            Node(
                package="clearsky_os_darkspace_integration",
                executable="darkspace_audit_node",
                name="darkspace_audit_node",
                output="screen",
                prefix="python3",
            )
        ]
    )
