cmake_minimum_required(VERSION 3.16)
project(fusion_node)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_pytest REQUIRED)

install(PROGRAMS
  nodes/fusion_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME fusion_node
)

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  ament_add_pytest_test(test_fusion_math tests/test_fusion_math.py)
endif()

ament_package()
