cmake_minimum_required(VERSION 3.16)
project(data_generation)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_pytest REQUIRED)

install(PROGRAMS
  scripts/synthetic_dataset_pipeline.py
  scripts/training_pipeline.py
  scripts/model_export_pipeline.py
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY
  scripts
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  ament_add_pytest_test(test_data_pipelines tests/test_data_pipelines.py)
endif()

ament_package()
