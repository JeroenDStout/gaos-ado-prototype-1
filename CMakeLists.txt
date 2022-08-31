#
# Initial set-up
#

cmake_minimum_required(VERSION 3.15)

project(Core)

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib")

# Languages
include(cmake/cxx.cmake)
include(cmake/python.cmake)

# Support
include(cmake/sources.cmake)

#
# Base config
#

 # intentionally left blank

#
# Paths
#

 # intentionally left blank

#
# Subprojects
#

add_subdirectory(src/version)
add_subdirectory(src/ado)

message(STATUS "")