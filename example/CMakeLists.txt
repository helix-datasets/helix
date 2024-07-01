cmake_minimum_required(VERSION 2.6)

project(example)

include_directories(SYSTEM )

add_executable(example main.cpp)
target_link_libraries(example )
