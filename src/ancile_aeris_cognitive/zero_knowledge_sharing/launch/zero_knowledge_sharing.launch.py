from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package="zero_knowledge_sharing",
            executable="zero_knowledge_sharing_node",
            name="zero_knowledge_sharing_node",
            output="screen",
        )
    ])
