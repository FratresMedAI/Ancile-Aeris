cmake_minimum_required(VERSION 3.16)
project(ancile_aeris_fusion)

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
find_package(ament_cmake_pytest REQUIRED)

install(PROGRAMS
  nodes/fusion_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME ancile_aeris_fusion_node
)

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  ament_add_pytest_test(test_ancile_aeris_fusion tests/test_ancile_aeris_fusion.py)
endif()

ament_package()
