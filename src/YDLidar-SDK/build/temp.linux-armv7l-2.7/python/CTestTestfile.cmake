# CMake generated Testfile for 
# Source directory: /home/ubuntu/F1bot/src/YDLidar-SDK/python
# Build directory: /home/ubuntu/F1bot/src/YDLidar-SDK/build/temp.linux-armv7l-2.7/python
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(ydlidar_py_test "/usr/bin/python" "/home/ubuntu/F1bot/src/YDLidar-SDK/python/test/pytest.py")
set_tests_properties(ydlidar_py_test PROPERTIES  ENVIRONMENT "PYTHONPATH=:/home/ubuntu/F1bot/src/YDLidar-SDK/build/temp.linux-armv7l-2.7/python")
subdirs("examples")
