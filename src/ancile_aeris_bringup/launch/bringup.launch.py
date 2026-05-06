from pathlib import Path

import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.substitutions import FindPackageShare


FEATURE_DEFAULTS = {
    "enable_video_analytics": "true",
    "enable_neuromorphic_sim": "true",
    "enable_hyperspectral_stub": "true",
    "enable_adversarial_defense": "true",
    "enable_cognitive_ew": "true",
    "enable_agent_orchestrator": "true",
    "enable_swarm_orchestrator": "true",
    "enable_digital_twin": "true",
    "enable_causal_xai": "true",
    "enable_verification": "true",
    "enable_copilot": "true",
    "enable_federated_learning": "true",
    "enable_continual_learning": "true",
    "enable_defensive_swarm_coordinator": "true",
    "enable_zero_knowledge_sharing": "true",
    "enable_resilient_pnt": "true",
    "enable_generative_red_team": "true",
    "enable_scout_mothership": "true",
    "enable_baby_interceptor": "false",
}


def _load_feature_defaults() -> dict[str, str]:
    defaults = dict(FEATURE_DEFAULTS)
    config_path = Path(get_package_share_directory("ancile_aeris_bringup")) / "config" / "payload_selector.yaml"
    if not config_path.exists():
        return defaults

    with config_path.open("r", encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file) or {}

    features = config.get("features", {})
    if not isinstance(features, dict):
        return defaults

    for feature_name in defaults:
        if feature_name in features:
            defaults[feature_name] = "true" if bool(features[feature_name]) else "false"
    return defaults


def _feature_arg(name: str, defaults: dict[str, str]) -> DeclareLaunchArgument:
    return DeclareLaunchArgument(name, default_value=defaults[name])


def _include(pkg: str, launch_file: str, condition=None):
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource([FindPackageShare(pkg), f"/launch/{launch_file}"]),
        condition=condition,
    )


def generate_launch_description() -> LaunchDescription:
    feature_defaults = _load_feature_defaults()
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
        _feature_arg("enable_video_analytics", feature_defaults),
        _feature_arg("enable_neuromorphic_sim", feature_defaults),
        _feature_arg("enable_hyperspectral_stub", feature_defaults),
        _feature_arg("enable_adversarial_defense", feature_defaults),
        _feature_arg("enable_cognitive_ew", feature_defaults),
        _feature_arg("enable_agent_orchestrator", feature_defaults),
        _feature_arg("enable_swarm_orchestrator", feature_defaults),
        _feature_arg("enable_digital_twin", feature_defaults),
        _feature_arg("enable_causal_xai", feature_defaults),
        _feature_arg("enable_verification", feature_defaults),
        _feature_arg("enable_copilot", feature_defaults),
        _feature_arg("enable_federated_learning", feature_defaults),
        _feature_arg("enable_continual_learning", feature_defaults),
        _feature_arg("enable_defensive_swarm_coordinator", feature_defaults),
        _feature_arg("enable_zero_knowledge_sharing", feature_defaults),
        _feature_arg("enable_resilient_pnt", feature_defaults),
        _feature_arg("enable_generative_red_team", feature_defaults),
        _feature_arg("enable_scout_mothership", feature_defaults),
        _feature_arg("enable_baby_interceptor", feature_defaults),

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
