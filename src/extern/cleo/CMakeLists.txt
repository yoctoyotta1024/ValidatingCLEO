# set cmake version
if(NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
  cmake_minimum_required(VERSION 3.18.0)
endif()

# fetch and make cleo library available
include(FetchContent)
FetchContent_Declare(
  cleo
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  URL https://github.com/yoctoyotta1024/CLEO/archive/refs/tags/v0.39.1.zip
  GIT_TAG 8ac373ae5827d77db737c20f24917c80c3d0dc07
)
FetchContent_MakeAvailable(cleo)

message(STATUS "CLEO version v0.39.1, installation in: ${CLEO_BINARY_DIR}")
