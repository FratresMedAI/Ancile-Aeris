from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.substitutions import FindPackageShare


def generate_launch_description() -> LaunchDescription:
    sim_mode = LaunchConfiguration('sim_mode')
    payload = LaunchConfiguration('payload')
    sensor_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('sensor_nodes'),
            '/launch/sensor_nodes.launch.py',
        ])
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'sim_mode',
            default_value='true',
            description='Run Ancile-Aeris in simulation mode'
        ),
        DeclareLaunchArgument(
            'payload',
            default_value='cuas',
            description='Payload profile: cuas, perimeter_ct_cuas, or generic',
        ),
        LogInfo(msg=['Launching Ancile-Aeris full system. sim_mode=', sim_mode, ' payload=', payload]),
        sensor_launch,
    ])
