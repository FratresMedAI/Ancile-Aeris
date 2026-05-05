cmake_minimum_required(VERSION 3.16)
project(ancile_aeris_safety_gate)

find_package(ament_cmake REQUIRED)

install(PROGRAMS
  nodes/ancile_aeris_safety_gate_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME ancile_aeris_safety_gate_node
)

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
