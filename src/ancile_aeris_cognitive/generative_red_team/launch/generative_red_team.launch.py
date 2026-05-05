from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="generative_red_team", executable="generative_red_team_node", name="generative_red_team_node", output="screen")
    ])
