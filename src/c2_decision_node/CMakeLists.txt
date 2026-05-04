cmake_minimum_required(VERSION 3.16)
project(c2_decision_node)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_pytest REQUIRED)

install(PROGRAMS
  nodes/c2_decision_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME c2_decision_node
)

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  ament_add_pytest_test(test_c2_scoring tests/test_c2_scoring.py)
endif()

ament_package()
