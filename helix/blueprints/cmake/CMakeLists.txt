cmake_minimum_required(VERSION 2.6)

project(${name})

include_directories(SYSTEM ${include_directories})

add_executable(${name} main.${extension})
target_link_libraries(${name} ${libraries})
