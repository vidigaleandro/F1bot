# CMake generated Testfile for 
# Source directory: /home/ubuntu/f1tenth_ws/src/f1tenth_system/YDLidar-SDK/python
# Build directory: /home/ubuntu/f1tenth_ws/src/f1tenth_system/YDLidar-SDK/src/python
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(ydlidar_py_test "/usr/bin/python" "/home/ubuntu/f1tenth_ws/src/f1tenth_system/YDLidar-SDK/python/test/pytest.py")
set_tests_properties(ydlidar_py_test PROPERTIES  ENVIRONMENT "PYTHONPATH=/opt/ros/melodic/lib/python2.7/dist-packages:/home/ubuntu/f1tenth_ws/src/f1tenth_system/YDLidar-SDK/src/python")
subdirs("examples")
