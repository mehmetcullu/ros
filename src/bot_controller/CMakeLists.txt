cmake_minimum_required(VERSION 3.8)
project(bot_controller)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Gerekli paketler
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED) # Düzeltildi

# Python paketini yükle - ${} kullanımı önemli
ament_python_install_package(${PROJECT_NAME})

# Launch ve config dosyaları
install(
  DIRECTORY config launch
  DESTINATION share/${PROJECT_NAME}
)

# Python scriptleri (Dizin yapına göre kontrol et: bot_controller/simple_controller.py)
install(PROGRAMS
  ${PROJECT_NAME}/simple_controller.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()