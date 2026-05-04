cmake_minimum_required(VERSION 3.16)
project(trajectory_node)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_pytest REQUIRED)

install(PROGRAMS
  nodes/trajectory_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME trajectory_node
)

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  ament_add_pytest_test(test_trajectory_projection tests/test_trajectory_projection.py)
endif()

ament_package()
