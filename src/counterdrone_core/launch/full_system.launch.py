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
    enable_agentic_c2 = LaunchConfiguration('enable_agentic_c2')
    enable_adversarial_defense = LaunchConfiguration('enable_adversarial_defense')
    enable_digital_twin_v2 = LaunchConfiguration('enable_digital_twin_v2')
    enable_cognitive_ew = LaunchConfiguration('enable_cognitive_ew')
    enable_federated_learning = LaunchConfiguration('enable_federated_learning')
    enable_verification = LaunchConfiguration('enable_verification')
    enable_neuromorphic_sim = LaunchConfiguration('enable_neuromorphic_sim')
    enable_video_analytics_v2 = LaunchConfiguration('enable_video_analytics_v2')
    enable_swarm_orchestrator = LaunchConfiguration('enable_swarm_orchestrator')
    enable_copilot_v2 = LaunchConfiguration('enable_copilot_v2')
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
    agent_orchestrator_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('agent_orchestrator'),
            '/launch/agent_orchestrator.launch.py',
        ]),
        condition=IfCondition(PythonExpression(["'", enable_agentic_c2, "' == 'true'"])),
    )
    adversarial_defense_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('adversarial_defense'),
            '/launch/adversarial_defense.launch.py',
        ]),
        condition=IfCondition(PythonExpression(["'", enable_adversarial_defense, "' == 'true'"])),
    )
    digital_twin_v2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('digital_twin'),
            '/launch/digital_twin.launch.py',
        ]),
        condition=IfCondition(PythonExpression(["'", enable_digital_twin_v2, "' == 'true'"])),
    )
    cognitive_ew_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('cognitive_ew'),
            '/launch/cognitive_ew.launch.py',
        ]),
        condition=IfCondition(PythonExpression(["'", enable_cognitive_ew, "' == 'true'"])),
    )
    federated_learning_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('federated_learning'),
            '/launch/federated_learning.launch.py',
        ]),
        condition=IfCondition(PythonExpression(["'", enable_federated_learning, "' == 'true'"])),
    )
    verification_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('verification'),
            '/launch/verification.launch.py',
        ]),
        condition=IfCondition(PythonExpression(["'", enable_verification, "' == 'true'"])),
    )
    neuromorphic_sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('neuromorphic_sim'),
            '/launch/neuromorphic_sim.launch.py',
        ]),
        condition=IfCondition(PythonExpression(["'", enable_neuromorphic_sim, "' == 'true'"])),
    )
    video_analytics_v2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('video_analytics'),
            '/launch/video_analytics.launch.py',
        ]),
        condition=IfCondition(PythonExpression(["'", enable_video_analytics_v2, "' == 'true'"])),
    )
    swarm_orchestrator_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('swarm_orchestrator'),
            '/launch/swarm_orchestrator.launch.py',
        ]),
        condition=IfCondition(PythonExpression(["'", enable_swarm_orchestrator, "' == 'true'"])),
    )
    copilot_v2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('copilot'),
            '/launch/copilot.launch.py',
        ]),
        condition=IfCondition(PythonExpression(["'", enable_copilot_v2, "' == 'true'"])),
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
        DeclareLaunchArgument('enable_agentic_c2', default_value='true'),
        DeclareLaunchArgument('enable_adversarial_defense', default_value='true'),
        DeclareLaunchArgument('enable_digital_twin_v2', default_value='true'),
        DeclareLaunchArgument('enable_cognitive_ew', default_value='true'),
        DeclareLaunchArgument('enable_federated_learning', default_value='true'),
        DeclareLaunchArgument('enable_verification', default_value='true'),
        DeclareLaunchArgument('enable_neuromorphic_sim', default_value='true'),
        DeclareLaunchArgument('enable_video_analytics_v2', default_value='true'),
        DeclareLaunchArgument('enable_swarm_orchestrator', default_value='true'),
        DeclareLaunchArgument('enable_copilot_v2', default_value='true'),
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
        agent_orchestrator_launch,
        adversarial_defense_launch,
        digital_twin_v2_launch,
        cognitive_ew_launch,
        federated_learning_launch,
        verification_launch,
        neuromorphic_sim_launch,
        video_analytics_v2_launch,
        swarm_orchestrator_launch,
        copilot_v2_launch,
    ])
