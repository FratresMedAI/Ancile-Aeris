from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.substitutions import FindPackageShare


def _include(pkg: str, launch_file: str, condition=None):
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource([FindPackageShare(pkg), f"/launch/{launch_file}"]),
        condition=condition,
    )


def generate_launch_description() -> LaunchDescription:
    enable_video_analytics = LaunchConfiguration("enable_video_analytics")
    enable_neuromorphic_sim = LaunchConfiguration("enable_neuromorphic_sim")
    enable_hyperspectral_stub = LaunchConfiguration("enable_hyperspectral_stub")
    enable_adversarial_defense = LaunchConfiguration("enable_adversarial_defense")
    enable_cognitive_ew = LaunchConfiguration("enable_cognitive_ew")
    enable_agent_orchestrator = LaunchConfiguration("enable_agent_orchestrator")
    enable_swarm_orchestrator = LaunchConfiguration("enable_swarm_orchestrator")
    enable_digital_twin = LaunchConfiguration("enable_digital_twin")
    enable_causal_xai = LaunchConfiguration("enable_causal_xai")
    enable_verification = LaunchConfiguration("enable_verification")
    enable_copilot = LaunchConfiguration("enable_copilot")
    enable_federated_learning = LaunchConfiguration("enable_federated_learning")
    enable_continual_learning = LaunchConfiguration("enable_continual_learning")
    enable_defensive_swarm_coordinator = LaunchConfiguration("enable_defensive_swarm_coordinator")
    enable_zero_knowledge_sharing = LaunchConfiguration("enable_zero_knowledge_sharing")
    enable_resilient_pnt = LaunchConfiguration("enable_resilient_pnt")
    enable_generative_red_team = LaunchConfiguration("enable_generative_red_team")
    enable_scout_mothership = LaunchConfiguration("enable_scout_mothership")
    enable_baby_interceptor = LaunchConfiguration("enable_baby_interceptor")

    actions = [
        DeclareLaunchArgument("enable_video_analytics", default_value="true"),
        DeclareLaunchArgument("enable_neuromorphic_sim", default_value="true"),
        DeclareLaunchArgument("enable_hyperspectral_stub", default_value="true"),
        DeclareLaunchArgument("enable_adversarial_defense", default_value="true"),
        DeclareLaunchArgument("enable_cognitive_ew", default_value="true"),
        DeclareLaunchArgument("enable_agent_orchestrator", default_value="true"),
        DeclareLaunchArgument("enable_swarm_orchestrator", default_value="true"),
        DeclareLaunchArgument("enable_digital_twin", default_value="true"),
        DeclareLaunchArgument("enable_causal_xai", default_value="true"),
        DeclareLaunchArgument("enable_verification", default_value="true"),
        DeclareLaunchArgument("enable_copilot", default_value="true"),
        DeclareLaunchArgument("enable_federated_learning", default_value="true"),
        DeclareLaunchArgument("enable_continual_learning", default_value="true"),
        DeclareLaunchArgument("enable_defensive_swarm_coordinator", default_value="true"),
        DeclareLaunchArgument("enable_zero_knowledge_sharing", default_value="true"),
        DeclareLaunchArgument("enable_resilient_pnt", default_value="true"),
        DeclareLaunchArgument("enable_generative_red_team", default_value="true"),
        DeclareLaunchArgument("enable_scout_mothership", default_value="true"),
        DeclareLaunchArgument("enable_baby_interceptor", default_value="false"),

        _include("ancile_aeris_sensors", "ancile_aeris_sensors.launch.py"),
        _include("ancile_aeris_fusion", "ancile_aeris_fusion.launch.py"),
        _include("ancile_aeris_safety_gate", "ancile_aeris_safety_gate.launch.py"),
        _include("ancile_aeris_sensor_resilience", "ancile_aeris_sensor_resilience.launch.py"),
        _include("ancile_aeris_swarm_intent", "ancile_aeris_swarm_intent.launch.py"),
        _include("ancile_aeris_operator_copilot", "ancile_aeris_operator_copilot.launch.py"),

        _include("video_analytics", "video_analytics.launch.py", IfCondition(enable_video_analytics)),
        _include("neuromorphic_sim", "neuromorphic_sim.launch.py", IfCondition(enable_neuromorphic_sim)),
        _include("hyperspectral_stub", "hyperspectral_stub.launch.py", IfCondition(enable_hyperspectral_stub)),
        _include("adversarial_defense", "adversarial_defense.launch.py", IfCondition(enable_adversarial_defense)),
        _include("cognitive_ew", "cognitive_ew.launch.py", IfCondition(enable_cognitive_ew)),
        _include("agent_orchestrator", "agent_orchestrator.launch.py", IfCondition(enable_agent_orchestrator)),
        _include("swarm_orchestrator", "swarm_orchestrator.launch.py", IfCondition(enable_swarm_orchestrator)),
        _include("digital_twin", "digital_twin.launch.py", IfCondition(enable_digital_twin)),
        _include("causal_xai", "causal_xai.launch.py", IfCondition(enable_causal_xai)),
        _include("verification", "verification.launch.py", IfCondition(enable_verification)),
        _include("copilot", "copilot.launch.py", IfCondition(enable_copilot)),
        _include("federated_learning", "federated_learning.launch.py", IfCondition(enable_federated_learning)),
        _include("continual_learning", "continual_learning.launch.py", IfCondition(enable_continual_learning)),
        _include("defensive_swarm_coordinator", "defensive_swarm_coordinator.launch.py", IfCondition(enable_defensive_swarm_coordinator)),
        _include("zero_knowledge_sharing", "zero_knowledge_sharing.launch.py", IfCondition(enable_zero_knowledge_sharing)),
        _include("resilient_pnt", "resilient_pnt.launch.py", IfCondition(enable_resilient_pnt)),
        _include("generative_red_team", "generative_red_team.launch.py", IfCondition(enable_generative_red_team)),
        _include("scout_mothership", "scout_mothership.launch.py", IfCondition(enable_scout_mothership)),
        _include("baby_interceptor", "baby_interceptor.launch.py", IfCondition(enable_baby_interceptor)),
    ]

    return LaunchDescription(actions)
