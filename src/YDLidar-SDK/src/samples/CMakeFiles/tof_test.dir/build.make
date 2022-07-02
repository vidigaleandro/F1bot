# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/ubuntu/f1tenth_ws/src/f1tenth_system/YDLidar-SDK

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/ubuntu/f1tenth_ws/src/f1tenth_system/YDLidar-SDK/src

# Include any dependencies generated for this target.
include samples/CMakeFiles/tof_test.dir/depend.make

# Include the progress variables for this target.
include samples/CMakeFiles/tof_test.dir/progress.make

# Include the compile flags for this target's objects.
include samples/CMakeFiles/tof_test.dir/flags.make

samples/CMakeFiles/tof_test.dir/tof_test.cpp.o: samples/CMakeFiles/tof_test.dir/flags.make
samples/CMakeFiles/tof_test.dir/tof_test.cpp.o: ../samples/tof_test.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/ubuntu/f1tenth_ws/src/f1tenth_system/YDLidar-SDK/src/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object samples/CMakeFiles/tof_test.dir/tof_test.cpp.o"
	cd /home/ubuntu/f1tenth_ws/src/f1tenth_system/YDLidar-SDK/src/samples && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/tof_test.dir/tof_test.cpp.o -c /home/ubuntu/f1tenth_ws/src/f1tenth_system/YDLidar-SDK/samples/tof_test.cpp

samples/CMakeFiles/tof_test.dir/tof_test.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/tof_test.dir/tof_test.cpp.i"
	cd /home/ubuntu/f1tenth_ws/src/f1tenth_system/YDLidar-SDK/src/samples && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/ubuntu/f1tenth_ws/src/f1tenth_system/YDLidar-SDK/samples/tof_test.cpp > CMakeFiles/tof_test.dir/tof_test.cpp.i

samples/CMakeFiles/tof_test.dir/tof_test.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/tof_test.dir/tof_test.cpp.s"
	cd /home/ubuntu/f1tenth_ws/src/f1tenth_system/YDLidar-SDK/src/samples && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/ubuntu/f1tenth_ws/src/f1tenth_system/YDLidar-SDK/samples/tof_test.cpp -o CMakeFiles/tof_test.dir/tof_test.cpp.s

samples/CMakeFiles/tof_test.dir/tof_test.cpp.o.requires:

.PHONY : samples/CMakeFiles/tof_test.dir/tof_test.cpp.o.requires

samples/CMakeFiles/tof_test.dir/tof_test.cpp.o.provides: samples/CMakeFiles/tof_test.dir/tof_test.cpp.o.requires
	$(MAKE) -f samples/CMakeFiles/tof_test.dir/build.make samples/CMakeFiles/tof_test.dir/tof_test.cpp.o.provides.build
.PHONY : samples/CMakeFiles/tof_test.dir/tof_test.cpp.o.provides

samples/CMakeFiles/tof_test.dir/tof_test.cpp.o.provides.build: samples/CMakeFiles/tof_test.dir/tof_test.cpp.o


# Object files for target tof_test
tof_test_OBJECTS = \
"CMakeFiles/tof_test.dir/tof_test.cpp.o"

# External object files for target tof_test
tof_test_EXTERNAL_OBJECTS =

tof_test: samples/CMakeFiles/tof_test.dir/tof_test.cpp.o
tof_test: samples/CMakeFiles/tof_test.dir/build.make
tof_test: libydlidar_sdk.a
tof_test: samples/CMakeFiles/tof_test.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/ubuntu/f1tenth_ws/src/f1tenth_system/YDLidar-SDK/src/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../tof_test"
	cd /home/ubuntu/f1tenth_ws/src/f1tenth_system/YDLidar-SDK/src/samples && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/tof_test.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
samples/CMakeFiles/tof_test.dir/build: tof_test

.PHONY : samples/CMakeFiles/tof_test.dir/build

samples/CMakeFiles/tof_test.dir/requires: samples/CMakeFiles/tof_test.dir/tof_test.cpp.o.requires

.PHONY : samples/CMakeFiles/tof_test.dir/requires

samples/CMakeFiles/tof_test.dir/clean:
	cd /home/ubuntu/f1tenth_ws/src/f1tenth_system/YDLidar-SDK/src/samples && $(CMAKE_COMMAND) -P CMakeFiles/tof_test.dir/cmake_clean.cmake
.PHONY : samples/CMakeFiles/tof_test.dir/clean

samples/CMakeFiles/tof_test.dir/depend:
	cd /home/ubuntu/f1tenth_ws/src/f1tenth_system/YDLidar-SDK/src && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/ubuntu/f1tenth_ws/src/f1tenth_system/YDLidar-SDK /home/ubuntu/f1tenth_ws/src/f1tenth_system/YDLidar-SDK/samples /home/ubuntu/f1tenth_ws/src/f1tenth_system/YDLidar-SDK/src /home/ubuntu/f1tenth_ws/src/f1tenth_system/YDLidar-SDK/src/samples /home/ubuntu/f1tenth_ws/src/f1tenth_system/YDLidar-SDK/src/samples/CMakeFiles/tof_test.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : samples/CMakeFiles/tof_test.dir/depend

