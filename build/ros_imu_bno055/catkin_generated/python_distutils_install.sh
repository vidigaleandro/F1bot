#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/ubuntu/F1bot/src/ros_imu_bno055"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/ubuntu/F1bot/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/ubuntu/F1bot/install/lib/python3/dist-packages:/home/ubuntu/F1bot/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/ubuntu/F1bot/build" \
    "/usr/bin/python3" \
    "/home/ubuntu/F1bot/src/ros_imu_bno055/setup.py" \
     \
    build --build-base "/home/ubuntu/F1bot/build/ros_imu_bno055" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/ubuntu/F1bot/install" --install-scripts="/home/ubuntu/F1bot/install/bin"
