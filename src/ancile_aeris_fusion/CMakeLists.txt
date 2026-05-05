cmake_minimum_required(VERSION 3.16)
project(ancile_aeris_fusion)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_pytest REQUIRED)

install(PROGRAMS
  nodes/fusion_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME ancile_aeris_fusion_node
)

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  ament_add_pytest_test(test_ancile_aeris_fusion tests/test_ancile_aeris_fusion.py)
endif()

ament_package()
