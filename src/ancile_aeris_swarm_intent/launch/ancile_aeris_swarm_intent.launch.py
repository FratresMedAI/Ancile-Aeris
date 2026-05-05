from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package="ancile_aeris_swarm_intent",
            executable="ancile_aeris_swarm_intent_node",
            name="ancile_aeris_swarm_intent_node",
            output="screen",
            prefix="python3",
        ),
    ])
