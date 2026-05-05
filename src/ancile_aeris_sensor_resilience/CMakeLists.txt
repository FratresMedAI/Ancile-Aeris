cmake_minimum_required(VERSION 3.16)
project(ancile_aeris_sensor_resilience)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_pytest REQUIRED)

install(PROGRAMS
  nodes/sensor_resilience_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME ancile_aeris_sensor_resilience_node
)

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  ament_add_pytest_test(test_ancile_aeris_sensor_resilience tests/test_ancile_aeris_sensor_resilience.py)
endif()

ament_package()
