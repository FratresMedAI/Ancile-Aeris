from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="dashboard_node", executable="dashboard_bridge_node", name="dashboard_bridge_node", output="screen"),
    ])
