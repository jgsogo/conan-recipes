cmake_minimum_required(VERSION 3.4)
project(wrapper CXX)

include(conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

add_subdirectory(source_subfolder)
