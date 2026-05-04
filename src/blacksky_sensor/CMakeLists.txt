cmake_minimum_required(VERSION 3.16)
project(blacksky_sensor)

find_package(ament_cmake REQUIRED)

install(PROGRAMS
  nodes/blacksky_fusion_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME blacksky_fusion_node
)

install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
