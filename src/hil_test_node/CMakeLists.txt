cmake_minimum_required(VERSION 3.16)
project(hil_test_node)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_pytest REQUIRED)

install(PROGRAMS
  nodes/hil_test_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME hil_test_node
)

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  ament_add_pytest_test(test_hil_status tests/test_hil_status.py)
endif()

ament_package()
