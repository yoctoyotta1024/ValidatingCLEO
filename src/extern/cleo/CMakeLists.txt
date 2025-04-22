# set cmake version
if(NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
  cmake_minimum_required(VERSION 3.18.0)
endif()

# fetch and make cleo library available
include(FetchContent)
FetchContent_Declare(
  cleo
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  URL https://github.com/yoctoyotta1024/CLEO/archive/refs/tags/v0.39.7.zip
  GIT_TAG b89e4a15599b293b5086e6ec25164ca033578c9a
)
FetchContent_MakeAvailable(cleo)

message(STATUS "CLEO version v0.39.7, installation in: ${CLEO_BINARY_DIR}")
