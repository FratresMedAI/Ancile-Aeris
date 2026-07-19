cmake_minimum_required(VERSION 3.16)
project(clearsky_os_interfaces)

# Force clean cache on path mismatch (Docker bind-mount vs stale CMAKE_HOME_DIRECTORY)
if(EXISTS "${CMAKE_CURRENT_BINARY_DIR}/CMakeCache.txt")
  file(STRINGS "${CMAKE_CURRENT_BINARY_DIR}/CMakeCache.txt" _cm_cache_line REGEX "^CMAKE_HOME_DIRECTORY:INTERNAL=" LIMIT_COUNT 1)
  if(_cm_cache_line)
    string(REGEX REPLACE "^CMAKE_HOME_DIRECTORY:INTERNAL=(.*)$" "\1" _cm_cached_src "${_cm_cache_line}")
    if(NOT _cm_cached_src STREQUAL "${CMAKE_SOURCE_DIR}")
      file(REMOVE "${CMAKE_CURRENT_BINARY_DIR}/CMakeCache.txt")
      file(REMOVE_RECURSE "${CMAKE_CURRENT_BINARY_DIR}/CMakeFiles")
    endif()
  endif()
endif()

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
