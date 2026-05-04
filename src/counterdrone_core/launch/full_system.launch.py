from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, LogInfo
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.substitutions import FindPackageShare


def generate_launch_description() -> LaunchDescription:
    sim_mode = LaunchConfiguration('sim_mode')
    payload = LaunchConfiguration('payload')
    video_enhanced = LaunchConfiguration('video_enhanced')
    cuas_enabled = IfCondition(PythonExpression(["'", payload, "' == 'cuas'"]))
    generic_enabled = IfCondition(PythonExpression(["'", payload, "' == 'generic'"]))
    cuas_or_generic_enabled = IfCondition(PythonExpression(["'", payload, "' in ['cuas','generic']"]))

    sensor_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('sensor_nodes'),
            '/launch/sensor_nodes.launch.py',
        ]),
        condition=cuas_or_generic_enabled,
    )
    fusion_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('fusion_node'),
            '/launch/fusion_node.launch.py',
        ]),
        condition=cuas_or_generic_enabled,
    )
    trajectory_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('trajectory_node'),
            '/launch/trajectory_node.launch.py',
        ]),
        condition=cuas_enabled,
    )
    ew_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('ew_node'),
            '/launch/ew_node.launch.py',
        ]),
        condition=cuas_enabled,
    )
    cyber_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('cyber_node'),
            '/launch/cyber_node.launch.py',
        ]),
        condition=cuas_or_generic_enabled,
    )
    swarm_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('swarm_sim_node'),
            '/launch/swarm_sim_node.launch.py',
        ]),
        condition=cuas_enabled,
    )
    swarm_intent_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('swarm_intent_node'),
            '/launch/swarm_intent.launch.py',
        ]),
        condition=cuas_or_generic_enabled,
    )
    dashboard_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('dashboard_node'),
            '/launch/dashboard_node.launch.py',
        ])
    )
    digital_twin_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('digital_twin_node'),
            '/launch/digital_twin_node.launch.py',
        ]),
        condition=cuas_or_generic_enabled,
    )
    hil_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('hil_test_node'),
            '/launch/hil_test_node.launch.py',
        ]),
        condition=cuas_enabled,
    )
    c2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('c2_decision_node'),
            '/launch/c2_decision_node.launch.py',
        ]),
        condition=cuas_or_generic_enabled,
    )
    copilot_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('operator_copilot_node'),
            '/launch/operator_copilot.launch.py',
        ]),
        condition=cuas_or_generic_enabled,
    )
    resilience_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('sensor_resilience_node'),
            '/launch/sensor_resilience.launch.py',
        ]),
        condition=cuas_or_generic_enabled,
    )
    video_analytics_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('video_analytics_node'),
            '/launch/video_analytics.launch.py',
        ]),
        condition=IfCondition(
            PythonExpression(["'", payload, "' == 'cuas' and '", video_enhanced, "' == 'true'"])
        ),
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'sim_mode',
            default_value='true',
            description='Run Ancile-Aeris in simulation mode',
        ),
        DeclareLaunchArgument(
            'payload',
            default_value='cuas',
            description='Payload profile: cuas, conservation, or generic',
        ),
        DeclareLaunchArgument(
            'video_enhanced',
            default_value='false',
            description='Enable video analytics payload overlay for cuas profile',
        ),
        LogInfo(msg=['Launching Ancile-Aeris full system. sim_mode=', sim_mode, ' payload=', payload]),
        LogInfo(
            msg=[
                'Conservation payload currently executes copied reference nodes in payloads/conservation; ',
                'ROS launch graph remains monitor-safe with dashboard visibility.',
            ],
            condition=IfCondition(PythonExpression(["'", payload, "' == 'conservation'"])),
        ),
        sensor_launch,
        fusion_launch,
        trajectory_launch,
        ew_launch,
        cyber_launch,
        swarm_launch,
        swarm_intent_launch,
        dashboard_launch,
        digital_twin_launch,
        hil_launch,
        c2_launch,
        video_analytics_launch,
        copilot_launch,
        resilience_launch,
    ])
