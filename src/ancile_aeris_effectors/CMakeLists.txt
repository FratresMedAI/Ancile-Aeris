cmake_minimum_required(VERSION 3.16)
project(ancile_aeris_effectors)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_pytest REQUIRED)

install(PROGRAMS
  nodes/effector_policy_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME effector_policy_node
)

install(PROGRAMS
  nodes/effector_sim_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME effector_sim_node
)

install(DIRECTORY launch config DESTINATION share/${PROJECT_NAME})

if(BUILD_TESTING)
  ament_add_pytest_test(test_effector_policy tests/test_effector_policy.py)
endif()

ament_package()
