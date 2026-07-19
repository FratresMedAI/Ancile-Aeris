from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package="agent_orchestrator",
            executable="agent_orchestrator_node",
            name="agent_orchestrator_node",
            output="screen",
        )
    ])
