cmake_minimum_required(VERSION 3.16)
project(blacksky_cyber)

find_package(ament_cmake REQUIRED)

install(PROGRAMS
  nodes/cyber_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME cyber_node
)

install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
