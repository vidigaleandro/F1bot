# CMake generated Testfile for 
# Source directory: /home/ubuntu/F1bot/src/YDLidar-SDK/python
# Build directory: /home/ubuntu/F1bot/src/YDLidar-SDK/build/python
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(ydlidar_py_test "/usr/bin/python" "/home/ubuntu/F1bot/src/YDLidar-SDK/python/test/pytest.py")
set_tests_properties(ydlidar_py_test PROPERTIES  ENVIRONMENT "PYTHONPATH=/home/ubuntu/F1bot/devel/lib/python3/dist-packages:/opt/ros/melodic/lib/python2.7/dist-packages:/home/ubuntu/F1bot/src/YDLidar-SDK/build/python")
subdirs("examples")
