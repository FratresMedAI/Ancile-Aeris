cmake_minimum_required(VERSION 3.16)
project(ancile_aeris_interfaces)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)
find_package(builtin_interfaces REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/ThreatAssessment.msg"
  "msg/MitigationRecommendation.msg"
  "msg/SensorHealth.msg"
  "msg/AdversarialAlert.msg"
  "msg/AgentProposal.msg"
  "msg/DigitalTwinResult.msg"
  "msg/SafetyViolation.msg"
  "msg/VerifiedAction.msg"
  "msg/CognitiveEWCommand.msg"
  "msg/NeuromorphicEvent.msg"
  "msg/HyperspectralObservation.msg"
  "msg/CausalExplanation.msg"
  "msg/ContinualLearningStatus.msg"
  "msg/ThreatIntelShare.msg"
  "msg/ResilientPntEstimate.msg"
  "msg/RedTeamScenario.msg"
  "msg/ScoutTrack.msg"
  "msg/InterceptorStatus.msg"
  "msg/EngagementResult.msg"
  "srv/RequestModelUpdate.srv"
  "srv/QueryCopilot.srv"
  "srv/ShareThreatIntel.srv"
  "srv/RequestInterceptorAuthorization.srv"
  "action/ExecuteMitigation.action"
  DEPENDENCIES std_msgs builtin_interfaces
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()
