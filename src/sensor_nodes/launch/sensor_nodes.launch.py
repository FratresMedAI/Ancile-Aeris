from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="sensor_nodes", executable="visual_node", name="visual_node", output="screen"),
        Node(package="sensor_nodes", executable="acoustic_node", name="acoustic_node", output="screen"),
        Node(package="sensor_nodes", executable="rf_node", name="rf_node", output="screen"),
        Node(package="sensor_nodes", executable="lidar_node", name="lidar_node", output="screen"),
        Node(package="sensor_nodes", executable="sigint_node", name="sigint_node", output="screen"),
    ])
