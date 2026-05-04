from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package="swarm_intent_node",
            executable="swarm_intent_node",
            name="swarm_intent_node",
            output="screen",
        ),
    ])
