import os.path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def _launch_fob_swarm(context, *args, **kwargs):
    share_dir = get_package_share_directory("scout_mothership")
    config_yaml = os.path.join(share_dir, "config", "scout_config.yaml")
    count = int(LaunchConfiguration("fob_count").perform(context))
    count = max(2, min(4, count))
    mesh_enabled = LaunchConfiguration("mesh_enabled").perform(context).lower() in ("true", "1", "yes")

    nodes = []
    for i in range(count):
        mid = f"mhs-{i+1:03d}"
        nodes.append(
            Node(
                package="scout_mothership",
                executable="scout_mothership_node",
                name=f"scout_mothership_{i+1:03d}",
                output="screen",
                prefix="python3",
                parameters=[
                    config_yaml,
                    {
                        "mothership_id": mid,
                        "mesh_enabled": mesh_enabled,
                        "mesh_peer_count": count,
                        "enable_mesh_publish": mesh_enabled,
                    },
                ],
            )
        )

    nodes.append(
        Node(
            package="scout_mothership",
            executable="fob_coordinator_node",
            name="fob_coordinator_node",
            output="screen",
            prefix="python3",
            parameters=[
                {
                    "fob_count": count,
                    "micro_capacity_per_fob": int(
                        LaunchConfiguration("micro_capacity_per_fob").perform(context)
                    ),
                    "publish_hz": float(LaunchConfiguration("fob_publish_hz").perform(context)),
                    "mix_sensor_pod": int(LaunchConfiguration("mix_sensor_pod").perform(context)),
                    "mix_acoustic_disruptor": int(LaunchConfiguration("mix_acoustic_disruptor").perform(context)),
                    "mix_kevlar_web": int(LaunchConfiguration("mix_kevlar_web").perform(context)),
                    "mix_cognitive_ew_pod": int(LaunchConfiguration("mix_cognitive_ew_pod").perform(context)),
                    "mix_kamikaze_ram_slots": int(LaunchConfiguration("mix_kamikaze_ram_slots").perform(context)),
                    "profile": LaunchConfiguration("fob_profile").perform(context),
                }
            ],
        )
    )
    return nodes


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription(
        [
            DeclareLaunchArgument("mesh_enabled", default_value="true"),
            DeclareLaunchArgument("fob_count", default_value="3"),
            DeclareLaunchArgument("micro_capacity_per_fob", default_value="12"),
            DeclareLaunchArgument("fob_publish_hz", default_value="1.0"),
            DeclareLaunchArgument("fob_profile", default_value="mothership_fob_standard"),
            DeclareLaunchArgument("mix_sensor_pod", default_value="4"),
            DeclareLaunchArgument("mix_acoustic_disruptor", default_value="2"),
            DeclareLaunchArgument("mix_kevlar_web", default_value="2"),
            DeclareLaunchArgument("mix_cognitive_ew_pod", default_value="3"),
            DeclareLaunchArgument("mix_kamikaze_ram_slots", default_value="1"),
            OpaqueFunction(function=_launch_fob_swarm),
        ]
    )
