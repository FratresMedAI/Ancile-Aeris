import os.path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    share_dir = get_package_share_directory("baby_interceptor")
    config_yaml = os.path.join(share_dir, "config", "baby_interceptor.yaml")
    return LaunchDescription(
        [
            Node(
                package="baby_interceptor",
                executable="baby_interceptor_node",
                name="baby_interceptor_node",
                output="screen",
                prefix="python3",
                parameters=[config_yaml],
            )
        ]
    )
