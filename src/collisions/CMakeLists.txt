# set cmake version
if(NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
  cmake_minimum_required(VERSION 3.18.0)
endif()

# set project name and print directory of this CMakeLists.txt (source directory of project)
project("collisions")
message("PROJECT_SOURCE_DIR: ${PROJECT_SOURCE_DIR}")

# Set libraries from CLEO to link with executable
set(CLEOLIBS gridboxes initialise observers runcleo superdrops zarr)

### create primary executable 1 ###
set(exec colls_golovin)
add_executable(${exec} EXCLUDE_FROM_ALL "main_golovin.cpp")

# Add directories and link libraries to target
target_link_libraries(${exec} PRIVATE cartesiandomain "${CLEOLIBS}")
target_link_libraries(${exec} PUBLIC Kokkos::kokkos)
target_include_directories(${exec} PRIVATE "${CLEO_SOURCE_DIR}/libs") # CLEO libs directory

# set specific C++ compiler options for target (optional)
#target_compile_options(${exec} PRIVATE)

# set compiler properties for target(s)
set_target_properties(${exec} PROPERTIES
  CMAKE_CXX_STANDARD_REQUIRED ON
  CMAKE_CXX_EXTENSIONS ON
  CXX_STANDARD 20)

### create primary executable 2 ###
set(exec colls_long)
add_executable(${exec} EXCLUDE_FROM_ALL "main_long.cpp")

# Add directories and link libraries to target
target_link_libraries(${exec} PRIVATE cartesiandomain "${CLEOLIBS}")
target_link_libraries(${exec} PUBLIC Kokkos::kokkos)
target_include_directories(${exec} PRIVATE "${CLEO_SOURCE_DIR}/libs") # CLEO libs directory

# set specific C++ compiler options for target (optional)
#target_compile_options(${exec} PRIVATE)

# set compiler properties for target(s)
set_target_properties(${exec} PROPERTIES
  CMAKE_CXX_STANDARD_REQUIRED ON
  CMAKE_CXX_EXTENSIONS ON
  CXX_STANDARD 20)

### create primary executable 3 ###
set(exec colls_testikstraub)
add_executable(${exec} EXCLUDE_FROM_ALL "main_testikstraub.cpp")

# Add directories and link libraries to target
target_link_libraries(${exec} PRIVATE cartesiandomain "${CLEOLIBS}")
target_link_libraries(${exec} PUBLIC Kokkos::kokkos)
target_include_directories(${exec} PRIVATE "${CLEO_SOURCE_DIR}/libs") # CLEO libs directory

# set specific C++ compiler options for target (optional)
#target_compile_options(${exec} PRIVATE)

# set compiler properties for target(s)
set_target_properties(${exec} PROPERTIES
  CMAKE_CXX_STANDARD_REQUIRED ON
  CMAKE_CXX_EXTENSIONS ON
  CXX_STANDARD 20)
