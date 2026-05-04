cmake_minimum_required(VERSION 3.16)
project(swarm_intent_node)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_pytest REQUIRED)

install(PROGRAMS
  nodes/swarm_intent_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME swarm_intent_node
)

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  ament_add_pytest_test(test_swarm_intent tests/test_swarm_intent.py)
endif()

ament_package()
