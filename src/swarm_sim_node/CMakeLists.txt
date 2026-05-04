cmake_minimum_required(VERSION 3.16)
project(swarm_sim_node)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_pytest REQUIRED)

install(PROGRAMS
  nodes/swarm_sim_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME swarm_sim_node
)

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  ament_add_pytest_test(test_swarm_policy tests/test_swarm_policy.py)
endif()

ament_package()
