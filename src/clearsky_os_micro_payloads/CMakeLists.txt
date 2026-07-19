cmake_minimum_required(VERSION 3.16)
project(clearsky_os_micro_payloads)

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

install(PROGRAMS
  nodes/sensor_pod_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME sensor_pod_node
)
install(PROGRAMS
  nodes/acoustic_disruptor_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME acoustic_disruptor_node
)
install(PROGRAMS
  nodes/kevlar_web_deployer_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME kevlar_web_deployer_node
)
install(PROGRAMS
  nodes/cognitive_ew_pod_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME cognitive_ew_pod_node
)
install(PROGRAMS
  nodes/kamikaze_ram_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME kamikaze_ram_node
)

install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})
install(FILES resource/clearsky_os_micro_payloads DESTINATION share/ament_index/resource_index/packages)

ament_package()
