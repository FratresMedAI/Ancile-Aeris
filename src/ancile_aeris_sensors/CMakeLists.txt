cmake_minimum_required(VERSION 3.16)
project(ancile_aeris_sensors)

find_package(ament_cmake REQUIRED)

install(PROGRAMS
  nodes/visual_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME ancile_aeris_visual_node
)

install(PROGRAMS
  nodes/acoustic_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME ancile_aeris_acoustic_node
)

install(PROGRAMS
  nodes/rf_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME ancile_aeris_rf_node
)

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
