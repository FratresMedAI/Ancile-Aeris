cmake_minimum_required(VERSION 3.16)
project(ew_node)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_pytest REQUIRED)

install(PROGRAMS
  nodes/ew_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME ew_node
)

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  ament_add_pytest_test(test_ew_recommendation tests/test_ew_recommendation.py)
endif()

ament_package()
