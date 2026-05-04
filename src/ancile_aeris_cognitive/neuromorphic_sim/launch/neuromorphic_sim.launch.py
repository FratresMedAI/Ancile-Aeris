from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="neuromorphic_sim", executable="neuromorphic_sim_node", name="neuromorphic_sim_node", output="screen")
    ])
