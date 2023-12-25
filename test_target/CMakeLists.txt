cmake_minimum_required(VERSION 3.17)

project(
  Example 
  VERSION 1.0
  LANGUAGES CXX)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g")

add_library(
    lib_a
    lib/src/lib.cpp
)

target_include_directories(lib_a PUBLIC lib/inc/)

add_executable(
    exe_a
    exe_a.cpp
)

target_link_libraries(exe_a PRIVATE lib_a)

add_executable(
    exe_b
    exe_b.cpp
)

target_link_libraries(exe_b PRIVATE lib_a)

