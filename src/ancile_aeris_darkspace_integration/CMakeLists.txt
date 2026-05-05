cmake_minimum_required(VERSION 3.16)
project(ancile_aeris_darkspace_integration)

find_package(ament_cmake REQUIRED)

install(PROGRAMS
  nodes/darkspace_audit_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME darkspace_audit_node
)

install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
