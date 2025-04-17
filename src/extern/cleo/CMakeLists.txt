# set cmake version
if(NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
  cmake_minimum_required(VERSION 3.18.0)
endif()

# fetch and make cleo library available
include(FetchContent)
FetchContent_Declare(
  cleo
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  URL https://github.com/yoctoyotta1024/CLEO/archive/refs/tags/v0.39.5.zip
  GIT_TAG 8fcb591c092f10fb4bb55a3064fbcf0bdee5dc74
)
FetchContent_MakeAvailable(cleo)

message(STATUS "CLEO version v0.39.5, installation in: ${CLEO_BINARY_DIR}")
