# set cmake version
if(NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
  cmake_minimum_required(VERSION 3.18.0)
endif()

# fetch and make cleo library available
include(FetchContent)
FetchContent_Declare(
  cleo
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  URL https://github.com/yoctoyotta1024/CLEO/archive/refs/heads/v0p39p7-paper2-edits-patch-applied.zip
  GIT_TAG fe1af8031f168c3d1978566108ee6c721404c02c
)
FetchContent_MakeAvailable(cleo)

message(STATUS "CLEO version v0.39.7 with patch applied, installation in: ${CLEO_BINARY_DIR}")
