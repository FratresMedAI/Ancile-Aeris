cmake_minimum_required(VERSION 3.16)
project(blacksky_darkspace_adapter)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_pytest REQUIRED)

install(PROGRAMS
  nodes/darkspace_adapter_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME darkspace_adapter_node
)

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  ament_add_pytest_test(test_darkspace_sign tests/test_darkspace_sign.py)
endif()

ament_package()
