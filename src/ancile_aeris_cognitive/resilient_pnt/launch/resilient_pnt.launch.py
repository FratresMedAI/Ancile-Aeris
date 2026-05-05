from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="resilient_pnt", executable="resilient_pnt_node", name="resilient_pnt_node", output="screen")
    ])
