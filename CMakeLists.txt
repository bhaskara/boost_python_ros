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



# set(GEN_DIR_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/munged/${PROJECT_NAME}_bp)
# set(GEN_SHARED_LIBRARY_DIR ${GEN_DIR_ROOT}/bindings)
# set(GEN_PYTHON_ROOT ${GEN_DIR_ROOT}/conversions)
set(GEN_DIR_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/munged)
set(GEN_SHARED_LIBRARY_DIR ${GEN_DIR_ROOT})
set(GEN_PYTHON_ROOT ${GEN_DIR_ROOT})

file(WRITE ${GEN_DIR_ROOT}/__init__.py "\n")
file(WRITE ${GEN_SHARED_LIBRARY_DIR}/__init__.py "\n")
file(WRITE ${GEN_PYTHON_ROOT}/__init__.py "\n")

add_definitions("-Wl,--no-undefined ")

rosbuild_add_library(rostime_boost_python src/rostime_exports.cpp)
set_target_properties(rostime_boost_python
  PROPERTIES
  PREFIX ""
)
target_link_libraries(rostime_boost_python 
  ${Boost_LIBRARIES}
  ${PYTHON_LIBRARIES}
  )


macro(bpmodule NAME)
    include_directories(
      ${PYTHON_INCLUDE_PATH}
      ${Boost_INCLUDE_DIRS}
    )

    add_library(${NAME}_cpp SHARED ${ARGN})
    message(STATUS "The libraries for ${NAME} are ${${PROJECT_NAME}_LIBRARIES}")
    target_link_libraries(${NAME}_cpp ${${PROJECT_NAME}_LIBRARIES})
    
    
    set_target_properties(${NAME}_cpp
      PROPERTIES
      OUTPUT_NAME ${NAME}_cpp
      LIBRARY_OUTPUT_DIRECTORY ${GEN_SHARED_LIBRARY_DIR}
      PREFIX ""
    )
    
    target_link_libraries(${NAME}_cpp
      ${Boost_LIBRARIES}
      ${PYTHON_LIBRARIES}
      rostime_boost_python
    )
endmacro()

macro(message_gen_wrap ROS_PACKAGE)
    set(GEN_DIR ${CMAKE_CURRENT_BINARY_DIR}/${ROS_PACKAGE}) #this is for generated cpp files.

    execute_process(COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/scripts/generate_pkg_bindings.py
      --package=${ROS_PACKAGE}
      --cpp_target_dir=${GEN_DIR}
      --py_target_dir=${GEN_PYTHON_ROOT}
      --current_package=${PROJECT_NAME}
    )

    file(GLOB ${ROS_PACKAGE}_srcs  ${GEN_DIR}/*.cpp)
    
    bpmodule(${ROS_PACKAGE}
        ${${ROS_PACKAGE}_srcs}
    )
endmacro()



message_gen_wrap(std_msgs)
message_gen_wrap(geometry_msgs)
message_gen_wrap(sensor_msgs)
