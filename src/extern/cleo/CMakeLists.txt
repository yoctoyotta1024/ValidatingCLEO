# set cmake version
if(NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
  cmake_minimum_required(VERSION 3.18.0)
endif()

# fetch and make cleo library available
include(FetchContent)
FetchContent_Declare(
  cleo
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  URL https://github.com/yoctoyotta1024/CLEO/archive/refs/tags/v0.39.6.zip
  GIT_TAG fd1d8eef7817f7dd9e8bea413802f013c6bbe5d4
)
FetchContent_MakeAvailable(cleo)

message(STATUS "CLEO version v0.39.6, installation in: ${CLEO_BINARY_DIR}")
