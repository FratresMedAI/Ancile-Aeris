from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description() -> LaunchDescription:
    share = get_package_share_directory("clearsky_os_sim")
    params = os.path.join(share, "config", "sim_truth_bridge.yaml")
    return LaunchDescription(
        [
            DeclareLaunchArgument("override_sensors", default_value="false"),
            Node(
                package="clearsky_os_sim",
                executable="sim_truth_bridge_node",
                name="sim_truth_bridge_node",
                output="screen",
                parameters=[
                    params,
                    {"override_sensors": LaunchConfiguration("override_sensors")},
                ],
                prefix="python3",
            ),
        ]
    )
