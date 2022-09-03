#!/usr/bin/env python


from tf.transformations import euler_from_quaternion
import tf
import rospy
import numpy as np
import math
from ackermann_msgs.msg import AckermannDriveStamped
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
from sensor_msgs.msg import Imu

# Variaveis Globais
speed = 0
orientation_list = None
x = 0
y = 0
speedM = [0, 0, 0, 0, 0]
x_speed = 0
y_speed = 0
roll = 0
pitch = 0
yaw = 0

odom_pub = rospy.Publisher("odom", Odometry, queue_size=1)
odom_broadcaster = tf.TransformBroadcaster()
rospy.init_node("Odometry", anonymous=True)
current_time = rospy.Time.now()
last_time = rospy.Time.now()


current_time = rospy.Time.now()
last_time = rospy.Time.now()


def callback(data):
    global speed
    speed = data.drive.speed

def callback2(data):
    global yaw, orientation_list, roll, pitch
    orientation_q = data.orientation
    orientation_list = [orientation_q.x, orientation_q.y,
                        orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion(orientation_list)

def listener():

    rospy.Subscriber('AcDrive', AckermannDriveStamped, callback)
    rospy.Subscriber('/imu/data', Imu, callback2)


def odometry_estimate():
    global speed, orientation_list, yaw, x, y,x_speed,y_speed, dt, last_time, roll, pitch
    odom = Odometry()
    while not rospy.is_shutdown():
        current_time = rospy.Time.now()
        dt = (current_time - last_time).to_sec()

        speedM.append(speed)
        sm = np.mean(speedM)
        speedM.pop(0)

        x_speed = speed * math.cos(yaw)
        print("Velocidade em X: ", x_speed)
        print("====================================================")
        print("cos", math.cos(yaw))
        print("SEN", math.sin(yaw))
        y_speed = speed * math.sin(yaw)
        print("Velocidade em Y: ", y_speed)
        print("====================================================")
        if speed < 5 * sm and speed > sm/5:
            x = x + 1*(x_speed * dt)
            y = y + 1*(y_speed * dt)
        print("Distancia em X: ", x)
        print("====================================================")
        print("Distancia em Y: ", y)
        print("====================================================")

        odom_quat = tf.transformations.quaternion_from_euler(roll, pitch, yaw)
        odom_broadcaster.sendTransform(
            (x, y, odom_quat[2]),
            odom_quat,
            current_time,
            "base_link",
            "odom"
        )

        odom.header.stamp = rospy.Time.now()
        odom.header.frame_id = "odom"

        odom.pose.pose = Pose(Point(x, y, 0.), Quaternion(*odom_quat))
        odom.child_frame_id = "base_link"
        odom.twist.twist = Twist(Vector3(x_speed, y_speed, 0), Vector3(0, 0, 0))
        odom_pub.publish(odom)

        last_time = current_time


if __name__ == '__main__':
    try:
        listener()
        odometry_estimate()

    except rospy.ROSInterruptException:
        rospy.logerr("ROS Interrupt Exception! Just ignore the exception!")
    #  pass
