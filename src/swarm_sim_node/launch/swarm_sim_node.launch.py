from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="swarm_sim_node", executable="swarm_sim_node", name="swarm_sim_node", output="screen"),
    ])
