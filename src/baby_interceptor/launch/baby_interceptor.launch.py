from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="baby_interceptor", executable="baby_interceptor_node", name="baby_interceptor_node", output="screen")
    ])
