cmake_minimum_required(VERSION 3.16)
project(blacksky_hmi)

find_package(ament_cmake REQUIRED)

install(PROGRAMS
  nodes/human_interface_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME human_interface_node
)

install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
