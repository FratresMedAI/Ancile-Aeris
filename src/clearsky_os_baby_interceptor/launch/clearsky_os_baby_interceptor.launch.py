import os.path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    share_dir = get_package_share_directory("clearsky_os_baby_interceptor")
    config_yaml = os.path.join(share_dir, "config", "interceptor_config.yaml")
    require_double_authorization = LaunchConfiguration("require_double_authorization")
    return LaunchDescription(
        [
            DeclareLaunchArgument("require_double_authorization", default_value="true"),
            Node(
                package="clearsky_os_baby_interceptor",
                executable="clearsky_os_baby_interceptor_node",
                name="clearsky_os_baby_interceptor_node",
                output="screen",
                prefix="python3",
                parameters=[config_yaml, {"require_double_authorization": require_double_authorization}],
            )
        ]
    )
