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
  "msg/CognitiveEwCommand.msg"
  "msg/NeuromorphicEvent.msg"
  "srv/RequestModelUpdate.srv"
  "srv/QueryCopilot.srv"
  "action/ExecuteMitigation.action"
  DEPENDENCIES std_msgs builtin_interfaces
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()
