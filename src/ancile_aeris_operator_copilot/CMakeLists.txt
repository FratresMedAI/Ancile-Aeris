cmake_minimum_required(VERSION 3.16)
project(ancile_aeris_operator_copilot)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_pytest REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/QueryCopilot.srv"
)

install(PROGRAMS
  nodes/operator_copilot_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME ancile_aeris_operator_copilot_node
)

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  ament_add_pytest_test(test_ancile_aeris_operator_copilot tests/test_ancile_aeris_operator_copilot.py)
endif()

ament_export_dependencies(rosidl_default_runtime)
ament_package()
