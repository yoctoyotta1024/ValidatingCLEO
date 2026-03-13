# set cmake version
if(NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
  cmake_minimum_required(VERSION 3.18.0)
endif()

# set project name and print directory of this CMakeLists.txt (source directory of project)
project("motion")
message("PROJECT_SOURCE_DIR: ${PROJECT_SOURCE_DIR}")

# Set libraries from CLEO to link with executable
set(CLEOLIBS gridboxes initialise observers runcleo superdrops zarr)

# create primary executable
set(exec motion)
add_executable(${exec} EXCLUDE_FROM_ALL "main.cpp")

# Add directories and link libraries to target
target_link_libraries(${exec} PRIVATE coupldyn_fromfile cartesiandomain "${CLEOLIBS}")
target_link_libraries(${exec} PUBLIC Kokkos::kokkos)
target_include_directories(${exec} PRIVATE "${CLEO_SOURCE_DIR}/libs") # CLEO libs directory

# set specific C++ compiler options for target (optional)
#target_compile_options(${exec} PRIVATE)

# set compiler properties for target(s)
set_target_properties(${exec} PROPERTIES
  CMAKE_CXX_STANDARD_REQUIRED ON
  CMAKE_CXX_EXTENSIONS ON
  CXX_STANDARD 20)

# create secondary executable
set(exec2 motion_with_tvel)
add_executable(${exec2} EXCLUDE_FROM_ALL "main_with_tvel.cpp")

# Add directories and link libraries to target
target_link_libraries(${exec2} PRIVATE coupldyn_fromfile cartesiandomain "${CLEOLIBS}")
target_link_libraries(${exec2} PUBLIC Kokkos::kokkos)
target_include_directories(${exec2} PRIVATE "${CLEO_SOURCE_DIR}/libs") # CLEO libs directory

# set specific C++ compiler options for target (optional)
#target_compile_options(${exec2} PRIVATE)

# set compiler properties for target(s)
set_target_properties(${exec2} PROPERTIES
  CMAKE_CXX_STANDARD_REQUIRED ON
  CMAKE_CXX_EXTENSIONS ON
  CXX_STANDARD 20)
