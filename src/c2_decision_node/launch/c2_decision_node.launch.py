from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="c2_decision_node", executable="c2_decision_node", name="c2_decision_node", output="screen"),
    ])
