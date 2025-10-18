cmake_minimum_required(VERSION 3.8)
project(ros_cpp)

# Set C++ standard
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# Create executables
add_executable(publisher src/publisher.cpp)
add_executable(subscriber src/subscriber.cpp)

# Link dependencies
ament_target_dependencies(publisher rclcpp std_msgs)
ament_target_dependencies(subscriber rclcpp std_msgs)

# Install targets
install(TARGETS
  publisher
  subscriber
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()