cmake_minimum_required(VERSION 2.8)
include($ENV{ROS_ROOT}/core/rosbuild/rosbuild.cmake)
rosbuild_init()

find_package(Threads REQUIRED)
find_package(Boost COMPONENTS
  python
  thread
  system
  REQUIRED
  )
find_package(PythonLibs REQUIRED)

macro(bpmodule NAME)    
    
    include_directories(
      ${PYTHON_INCLUDE_PATH}
      ${Boost_INCLUDE_DIRS}
    )
    
    rosbuild_add_library(${NAME}
      ${ARGN}
    )
      
    set_target_properties(${NAME}
      PROPERTIES
      OUTPUT_NAME ${NAME}
      PREFIX ""
    )
    
    target_link_libraries(${NAME}
      ${Boost_LIBRARIES}
      ${PYTHON_LIBRARIES}
    )
endmacro()

macro(message_gen_wrap ROS_PACKAGE)
    set(GEN_DIR ${CMAKE_CURRENT_BINARY_DIR}/${ROS_PACKAGE})
    #if(NOT ${ROS_PACKAGE}_srcs_cache)
        execute_process(COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/scripts/generate_pkg_bindings.py ${ROS_PACKAGE} ${GEN_DIR}
        )
    #    set(${ROS_PACKAGE}_srcs_cache ${ROS_PACKAGE}_srcs CACHE STRING "${ROS_PACKAGE} generated files")
    #endif()
    file(GLOB ${ROS_PACKAGE}_srcs  ${GEN_DIR}/*.cpp)
    bpmodule(${ROS_PACKAGE}
        ${${ROS_PACKAGE}_srcs}
    )
endmacro()

message_gen_wrap(sensor_msgs)
message_gen_wrap(geometry_msgs)
