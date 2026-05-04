cmake_minimum_required(VERSION 3.16)
project(blacksky_digital_twin)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_pytest REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/DigitalTwinSimulation.msg"
  "srv/SimulateAction.srv"
)

install(PROGRAMS
  nodes/digital_twin_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME digital_twin_node
)

install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  ament_add_pytest_test(test_sim_guard tests/test_sim_guard.py)
endif()

ament_export_dependencies(rosidl_default_runtime)
ament_package()
