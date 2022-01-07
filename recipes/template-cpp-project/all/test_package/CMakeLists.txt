cmake_minimum_required(VERSION 3.8)
project(test_package CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

find_package(template-cpp-project REQUIRED)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} template-cpp-project::template-cpp-project)
set_property(TARGET ${PROJECT_NAME} PROPERTY CXX_STANDARD 20)
