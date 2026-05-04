from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package="blacksky_sensor",
            executable="blacksky_fusion_node",
            name="blacksky_fusion_node",
            output="screen",
        ),
        Node(
            package="blacksky_core",
            executable="blacksky_core_node",
            name="blacksky_core_node",
            output="screen",
        ),
        Node(
            package="blacksky_hmi",
            executable="human_interface_node",
            name="human_interface_node",
            output="screen",
        ),
        Node(
            package="blacksky_cyber",
            executable="cyber_node",
            name="blacksky_cyber_node",
            output="screen",
        ),
        Node(
            package="blacksky_digital_twin",
            executable="digital_twin_node",
            name="blacksky_digital_twin_node",
            output="screen",
        ),
        Node(
            package="blacksky_darkspace_adapter",
            executable="darkspace_adapter_node",
            name="darkspace_adapter_node",
            output="screen",
        ),
    ])
