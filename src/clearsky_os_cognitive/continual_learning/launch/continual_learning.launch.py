from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="continual_learning", executable="continual_learning_node", name="continual_learning_node", output="screen")
    ])
