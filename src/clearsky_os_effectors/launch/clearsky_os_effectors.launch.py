import os.path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    share_dir = get_package_share_directory("clearsky_os_effectors")
    config_yaml = os.path.join(share_dir, "config", "effectors_config.yaml")
    enable_sim = LaunchConfiguration("enable_effector_sim")

    return LaunchDescription(
        [
            DeclareLaunchArgument("enable_effector_sim", default_value="true"),
            Node(
                package="clearsky_os_effectors",
                executable="effector_policy_node",
                name="effector_policy_node",
                output="screen",
                prefix="python3",
                parameters=[config_yaml],
            ),
            Node(
                package="clearsky_os_effectors",
                executable="effector_sim_node",
                name="effector_sim_node",
                output="screen",
                prefix="python3",
                parameters=[config_yaml],
                condition=IfCondition(enable_sim),
            ),
        ]
    )
