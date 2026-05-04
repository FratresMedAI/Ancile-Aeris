cmake_minimum_required(VERSION 3.16)
project(digital_twin_node)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_pytest REQUIRED)

install(PROGRAMS
  nodes/digital_twin_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME digital_twin_node
)

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  ament_add_pytest_test(test_digital_twin_state tests/test_digital_twin_state.py)
endif()

ament_package()
