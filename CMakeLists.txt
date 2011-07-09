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

set(GEN_DIR_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/munged)
set(BP_MSG_MODULE_NAME bp_ros_msgs)
set(BP_CONVERTER_MODULE_NAME bp_bridge)

file(WRITE ${GEN_DIR_ROOT}/${BP_MSG_MODULE_NAME}/__init__.py "\n")
file(WRITE ${GEN_DIR_ROOT}/${BP_CONVERTER_MODULE_NAME}/__init__.py "\n")

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
      LIBRARY_OUTPUT_DIRECTORY ${GEN_DIR_ROOT}/${BP_MSG_MODULE_NAME}
      PREFIX ""
    )
    
    target_link_libraries(${NAME}
      ${Boost_LIBRARIES}
      ${PYTHON_LIBRARIES}
    )
endmacro()

macro(message_gen_wrap ROS_PACKAGE)
    set(GEN_DIR ${CMAKE_CURRENT_BINARY_DIR}/${ROS_PACKAGE}) #this is for generated cpp files.
    set(GEN_PY_DIR ${GEN_DIR_ROOT}/${BP_CONVERTER_MODULE_NAME}/${ROS_PACKAGE})
    #generate an __init__.py fiile in the binary dir.
    file(WRITE ${GEN_PY_DIR}/__init__.py "\n")
    execute_process(COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/scripts/generate_pkg_bindings.py
      --package=${ROS_PACKAGE}
      --cpp_target_dir=${GEN_DIR}
      --py_target_dir=${GEN_PY_DIR}
    )

    file(GLOB ${ROS_PACKAGE}_srcs  ${GEN_DIR}/*.cpp)
    
    bpmodule(${ROS_PACKAGE}
        ${${ROS_PACKAGE}_srcs}
    )
endmacro()

message_gen_wrap(sensor_msgs)
message_gen_wrap(geometry_msgs)
