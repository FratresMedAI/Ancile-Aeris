cmake_minimum_required(VERSION 3.16)
project(blacksky_core)

find_package(ament_cmake REQUIRED)

install(PROGRAMS
  nodes/blacksky_core_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME blacksky_core_node
)

install(DIRECTORY
  include
  launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
