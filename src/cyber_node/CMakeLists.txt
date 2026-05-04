cmake_minimum_required(VERSION 3.16)
project(cyber_node)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_pytest REQUIRED)

install(PROGRAMS
  nodes/cyber_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME cyber_node
)

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  ament_add_pytest_test(test_cyber_identity tests/test_cyber_identity.py)
endif()

ament_package()
