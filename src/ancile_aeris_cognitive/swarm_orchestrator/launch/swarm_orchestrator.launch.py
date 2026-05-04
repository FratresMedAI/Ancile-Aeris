from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="swarm_orchestrator", executable="swarm_orchestrator_node", name="swarm_orchestrator_node", output="screen")
    ])
