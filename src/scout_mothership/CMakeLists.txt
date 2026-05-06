cmake_minimum_required(VERSION 3.16)
project(scout_mothership)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_pytest REQUIRED)

install(PROGRAMS scout_mothership/scout_node.py DESTINATION lib/${PROJECT_NAME} RENAME scout_mothership_node)
install(PROGRAMS nodes/scout_mothership_node.py DESTINATION lib/${PROJECT_NAME})
install(DIRECTORY launch config DESTINATION share/${PROJECT_NAME})

if(BUILD_TESTING)
  ament_add_pytest_test(test_scout_mothership tests/test_scout_mothership.py)
endif()

ament_package()
