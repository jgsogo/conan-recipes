cmake_minimum_required(VERSION 3.1)
project(test_package)

set(CONAN_CMAKE_SILENT_OUTPUT 1)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

find_package(imgui REQUIRED)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} imgui::imgui)
if (ADD_MISC)
    target_compile_definitions(${PROJECT_NAME} PRIVATE -DADD_MISC)
endif()
