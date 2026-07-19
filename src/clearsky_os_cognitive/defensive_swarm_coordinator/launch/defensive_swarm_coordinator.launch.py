from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package="defensive_swarm_coordinator",
            executable="defensive_swarm_coordinator_node",
            name="defensive_swarm_coordinator_node",
            output="screen",
        )
    ])
