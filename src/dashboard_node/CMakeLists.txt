cmake_minimum_required(VERSION 3.16)
project(dashboard_node)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_pytest REQUIRED)

install(PROGRAMS
  nodes/dashboard_bridge_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME dashboard_bridge_node
)

install(DIRECTORY
  launch
  config
  web
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  ament_add_pytest_test(test_dashboard_summary tests/test_dashboard_summary.py)
endif()

ament_package()
