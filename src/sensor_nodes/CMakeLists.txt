cmake_minimum_required(VERSION 3.16)
project(sensor_nodes)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_pytest REQUIRED)

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
  OPTIONAL
)

install(PROGRAMS
  nodes/visual_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME visual_node
)

install(PROGRAMS
  nodes/acoustic_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME acoustic_node
)

install(PROGRAMS
  nodes/rf_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME rf_node
)

install(PROGRAMS
  nodes/lidar_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME lidar_node
)

install(PROGRAMS
  nodes/sigint_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME sigint_node
)

if(BUILD_TESTING)
  ament_add_pytest_test(test_sensor_payloads tests/test_sensor_payloads.py)
endif()

ament_package()
