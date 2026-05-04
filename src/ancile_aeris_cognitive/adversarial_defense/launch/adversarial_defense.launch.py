from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="adversarial_defense", executable="adversarial_defense_node", name="adversarial_defense_node", output="screen")
    ])
