from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    mid = LaunchConfiguration("mothership_id")

    return LaunchDescription(
        [
            DeclareLaunchArgument("mothership_id", default_value="mhs-001"),
            Node(
                package="clearsky_os_micro_payloads",
                executable="sensor_pod_node",
                name="sensor_pod_node",
                output="screen",
                prefix="python3",
                parameters=[{"mothership_id": mid}],
            ),
            Node(
                package="clearsky_os_micro_payloads",
                executable="acoustic_disruptor_node",
                name="acoustic_disruptor_node",
                output="screen",
                prefix="python3",
                parameters=[{"mothership_id": mid}],
            ),
            Node(
                package="clearsky_os_micro_payloads",
                executable="kevlar_web_deployer_node",
                name="kevlar_web_deployer_node",
                output="screen",
                prefix="python3",
                parameters=[{"mothership_id": mid}],
            ),
            Node(
                package="clearsky_os_micro_payloads",
                executable="cognitive_ew_pod_node",
                name="cognitive_ew_pod_node",
                output="screen",
                prefix="python3",
                parameters=[{"mothership_id": mid}],
            ),
            Node(
                package="clearsky_os_micro_payloads",
                executable="kamikaze_ram_node",
                name="kamikaze_ram_node",
                output="screen",
                prefix="python3",
                parameters=[{"mothership_id": mid, "micro_id": "kamikaze-micro-001"}],
            ),
        ]
    )
