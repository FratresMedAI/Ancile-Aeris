cmake_minimum_required(VERSION 3.16)
project(video_analytics_node)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_pytest REQUIRED)

install(PROGRAMS
  nodes/video_analytics_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME video_analytics_node
)

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  ament_add_pytest_test(test_video_analytics tests/test_video_analytics.py)
endif()

ament_package()
