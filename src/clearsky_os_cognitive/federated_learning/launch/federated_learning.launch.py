from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="federated_learning", executable="federated_learning_node", name="federated_learning_node", output="screen")
    ])
