#!/usr/bin/env python

from visualization_msgs.msg import Marker
import sys
import numpy as np
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Vector3, Point, Quaternion, Pose, Twist
from ackermann_msgs.msg import AckermannDriveStamped
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Header, ColorRGBA
import math
import time
from std_srvs.srv import Empty
from tf.transformations import euler_from_quaternion, quaternion_from_euler

ack_publisher = None

tup = ([0, 0], [0, 0])
Fsen = np.asarray(tup)
yaw = 0
Fobs = [0, 0]
x =0
y= 0

markera = Marker()
markerb = Marker()
markerc = Marker()

linear_speed = 0

count = 0
linear_speed_med = 1
id = 0


def odom_callback(msg):
    global x, y, roll, pitch, yaw
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y,
                        orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion(orientation_list)


def scan_callback(msg):
    global Fobs

    Fobs = Fi(msg)


def Fi(data):
    global Fsen
    xa = 0
    ya = 0
    n = 3
    d = 0.15
    ran = np.asarray(data.ranges)
    ranz = ran.size
    #print('tamanho', ran.size)
    for i in range(0, 505, 1):
        if ran[i] > 0.15 and ran[i] < 5:

            xa += n*((ran[i]*math.cos((((i*360/ranz))*math.pi/180))
                     * 2*(d-ran[i]))/(d*ran[i]**4))
            ya += n*((ran[i]*math.sin((((i*360/ranz))*math.pi/180))
                     * 2*(d-ran[i]))/(d*ran[i]**4))

    Fsen[0] = ([-xa, -ya])

    return Fsen[0]


def go_to_goal(x_goal, y_goal):
    global x, y, yaw, Fsum, Fobs, linear_speed, line_point, count, linear_speed_med, marker, line_save, id

    markera = Marker()
    markera.header.frame_id = "/world"
    markerb = Marker()
    markerb.header.frame_id = "/world"
    markerc = Marker()
    markerc.header.frame_id = "/world"

    markera.type = markera.ARROW
    markera.action = markera.ADD
    markera.scale.x = 1
    markera.scale.y = 0.05
    markera.scale.z = 0.001
    markera.color.a = 1.0
    markera.color.r = 1.0
    markera.color.b = 0.0
    markera.pose.position.x = 0
    markera.pose.position.y = 0
    markera.pose.position.z = 1

    markerb.type = markerb.ARROW
    markerb.action = markerb.ADD
    markerb.scale.x = 0.5
    markerb.scale.y = 0.05
    markerb.scale.z = 0.001
    markerb.color.a = 1.0
    markerb.color.r = 0.0
    markerb.color.b = 1.0
    markerb.pose.position.x = 0
    markerb.pose.position.y = 0
    markerb.pose.position.z = 1

    markerc.type = markerc.ARROW
    markerc.action = markerc.ADD
    markerc.scale.x = 0.5
    markerc.scale.y = 0.05
    markerc.scale.z = 0.001
    markerc.color.a = 1.0
    markerc.color.r = 0.0
    markerc.color.g = 1.0
    markerc.pose.position.x = 0
    markerc.pose.position.y = 0
    markerc.pose.position.z = 1

    ack_msg = AckermannDriveStamped()
    ack_msg.header.stamp = rospy.Time.now()
    ack_msg.header.frame_id = ''
    ack_msg.drive.steering_angle = 0.0
    angular_yaw = 0
    max_steering_angle = 0.15
    max_speed = 1
    k = 20000000
    K_angular = 1
    speed = []

    while not rospy.is_shutdown():

        distance = abs(math.sqrt(((x_goal-x) ** 2) + ((y_goal-y) ** 2)))
        qx = (x_goal-x)
        qy = (y_goal-y)
        Fdist = [qx, qy]
        desired_angle_goal_dist = ((math.atan2(qy, qx)))

        Fobsmod = abs((math.sqrt(((Fobs[1]) ** 2) + ((Fobs[0]) ** 2)))/1)
        desired_angle_goal_obs = ((math.atan2(Fobs[1], Fobs[0])))
	print(yaw)
        if yaw < 0:
            yaw += 2*math.pi

        if desired_angle_goal_dist < 0:
            desired_angle_goal_dist += 2*math.pi

        if desired_angle_goal_obs < 0:
            desired_angle_goal_obs += 2*math.pi

        angular_yaw_dist = (desired_angle_goal_dist-yaw)

        angular_yaw_obs = (desired_angle_goal_obs)*K_angular

        (xo, yo, zo, wo) = quaternion_from_euler(0.0, 0.0, angular_yaw)

        markera.pose.orientation.x = xo
        markera.pose.orientation.y = yo
        markera.pose.orientation.z = zo
        markera.pose.orientation.w = wo

        (xo, yo, zo, wo) = quaternion_from_euler(0.0, 0.0, angular_yaw_dist)

        markerb.pose.orientation.x = xo
        markerb.pose.orientation.y = yo
        markerb.pose.orientation.z = zo
        markerb.pose.orientation.w = wo

        (xo, yo, zo, wo) = quaternion_from_euler(0.0, 0.0, angular_yaw_obs)

        markerc.pose.orientation.x = xo
        markerc.pose.orientation.y = yo
        markerc.pose.orientation.z = zo
        markerc.pose.orientation.w = wo

        Fdist[0] = (k*math.cos(angular_yaw_dist))
        Fdist[1] = (k*math.sin(angular_yaw_dist))

        Fobs[0] = Fobsmod*math.cos(angular_yaw_obs)
        Fobs[1] = Fobsmod*math.sin(angular_yaw_obs)

        Fsum = Fdist + Fobs
        #print (Fdist)
        angular_yaw = ((math.atan2((Fsum[1]), Fsum[0])))

        linear_speed = 0.5/((1+5*abs(angular_yaw)))
        if linear_speed < 0.40:
            linear_speed = 0.40

        # print linear_speed
	angular_yaw2 = angular_yaw
	print (angular_yaw)
        if angular_yaw2 > max_steering_angle:
            angular_yaw2 = 1*max_steering_angle
        if angular_yaw2 < (-1) * max_steering_angle:
            angular_yaw2 = 1*-max_steering_angle

        ack_msg.drive.speed = linear_speed
        ack_msg.drive.steering_angle = -angular_yaw2

        ack_publisher.publish(ack_msg)

        publishera.publish(markera)
        publisherb.publish(markerb)
        publisherc.publish(markerc)

        # print 'x=', x, 'y=',y, "yaw=",yaw, "desired=", angular_yaw

        time.sleep(0.01)
        if (distance < 1):
            break
    ack_msg.drive.speed = 0.0
    ack_publisher.publish(ack_msg)


if __name__ == '__main__':
    try:

        rospy.init_node('robot_motion_pose', anonymous=True)
        odom_sub = rospy.Subscriber('/odom', Odometry, odom_callback)
        publishera = rospy.Publisher('Result', Marker, queue_size=1)
        publisherb = rospy.Publisher('Distancia', Marker, queue_size=1)
        publisherc = rospy.Publisher('Parede', Marker, queue_size=1)
        scan_sub = rospy.Subscriber('scan', LaserScan, scan_callback)
        ack_publisher = rospy.Publisher(
            'Drive', AckermannDriveStamped, queue_size=1)

        time.sleep(2)

        #=======================COLUMBIA==================================#

        # go_to_goal(10,12)
        # go_to_goal(6,10)
        # go_to_goal(4,8)
        # go_to_goal(0,0)
        # go_to_goal(10,12)
        # go_to_goal(6,10)
        # go_to_goal(4,8)
        # go_to_goal(0,0)
        # go_to_goal(10,12)
        # go_to_goal(6,10)
        # go_to_goal(4,8)
        # go_to_goal(0,0)
        # go_to_goal(10,12)
        # go_to_goal(6,10)
        # go_to_goal(4,8)
        # go_to_goal(0,0)

        #=======================LEVINE===================================#

        go_to_goal(-6.0, 0)
        print("Next point")
        #go_to_goal(-8.5,1.0)
        #print("Next point")
        # go_to_goal(-13.8,8)
        #print("Next point")
        # go_to_goal(-13.8,0)
        #print("Next point")
        # go_to_goal(9.5,0)
        # go_to_goal(9.5,8.5)
        #print("Next point")
        # go_to_goal(-13.8,8)
        #print("Next point")
        # go_to_goal(-13.8,0)
        #print("Next point")
        # go_to_goal(9.5,0)
        # go_to_goal(9.5,8.5)
        #print("Next point")
        # go_to_goal(-13.8,8)
        #print("Next point")
        # go_to_goal(-13.8,0)
        #print("Next point")
        # go_to_goal(9.5,0)
        # go_to_goal(9.5,8.5)
        #print("Next point")
        # go_to_goal(-13.8,8)
        #print("Next point")
        # go_to_goal(-13.8,0)
        #print("Next point")
        # go_to_goal(9.5,0)

    #=======================MTL===================================#

        # go_to_goal(7.48,-2.5)
        # go_to_goal(7.99,4.8)
        # go_to_goal(0,6.1)
        # go_to_goal(-6.46,-3.13)
        # go_to_goal(1.62,-6.64)
        # go_to_goal(-1.05,1.48)
        # go_to_goal(7.48,-2.5)
        # go_to_goal(7.99,4.8)
        # go_to_goal(0,6.1)
        # go_to_goal(-6.46,-3.13)
        # go_to_goal(1.62,-6.64)
        # go_to_goal(-1.05,1.48)
        # go_to_goal(7.48,-2.5)
        # go_to_goal(7.99,4.8)
        # go_to_goal(0,6.1)
        # go_to_goal(-6.46,-3.13)
        # go_to_goal(1.62,-6.64)
        # go_to_goal(-1.05,1.48)
        # go_to_goal(7.48,-2.5)
        # go_to_goal(7.99,4.8)
        # go_to_goal(0,6.1)
        # go_to_goal(-6.46,-3.13)
        # go_to_goal(1.62,-6.64)
        # go_to_goal(-1.05,1.48)

    #=======================Berlin===================================#

        # go_to_goal(7.48,-11)
        # go_to_goal(3.2,-23)
        # go_to_goal(-0.2,-4.5)
        # go_to_goal(-4.6,-1.75)
        # go_to_goal(4,0)
        # go_to_goal(7.48,-11)
        # go_to_goal(3.2,-23)
        # go_to_goal(-0.2,-4.5)
        # go_to_goal(-4.6,-1.75)
        # go_to_goal(4,0)
        # go_to_goal(7.48,-11)
        # go_to_goal(3.2,-23)
        # go_to_goal(-0.2,-4.5)
        # go_to_goal(-4.6,-1.75)
        # go_to_goal(4,0)
        # go_to_goal(7.48,-11)
        # go_to_goal(3.2,-23)
        # go_to_goal(-0.2,-4.5)
        # go_to_goal(-4.6,-1.75)
        # go_to_goal(4,0)

    except rospy.ROSInterruptException:
        rospy.logdebug_throttle_identicalfo("node terminated.")
