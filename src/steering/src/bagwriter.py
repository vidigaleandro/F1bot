#!/usr/bin/env python
import rosbag

import rospy
from ackermann_msgs.msg import AckermannDriveStamped
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion

bag = rosbag.Bag('Dados.bag', 'w')

rospy.init_node('bagwriter', anonymous=True)

def callback(data):
    global speed
    speed = data.drive.speed

def callback2(data):
    global  x,y
    x = data.pose.pose.position.x
    y = data.pose.pose.position.y

def callback3(data):
    global  x2,y2
    x2 = data.pose.pose.position.x
    y2 = data.pose.pose.position.y

def listener():
    
    rospy.Subscriber('AcDrive', AckermannDriveStamped, callback)
    rospy.Subscriber("odometry/filtered", Odometry, callback2)
    rospy.Subscriber("odom_acker", Odometry, callback3)

def bag_write():
    global speed, x, y,teste
    speed = 0
    x = 0
    y = 0
    x2 = 0
    y2 = 0
    odometry2 = Odometry()
    odometry = Odometry()
    AcMsg = AckermannDriveStamped()
    r=rospy.Rate(100)
    while not rospy.is_shutdown():
        odometry.pose.pose = Pose(Point(x, y, 0.),Quaternion(0.,0.,0.,0.))
        odometry2.pose.pose = Pose(Point(x2, y2, 0.),Quaternion(0.,0.,0.,0.))
        AcMsg.drive.speed = speed

        bag.write('odom', odometry)
        bag.write('odom2', odometry2)
        bag.write('AcDrive', AcMsg)
    	r.sleep()
    
if __name__ == '__main__':
    try:
        listener()
        bag_write()

    except rospy.ROSInterruptException:
        rospy.logerr("ROS Interrupt Exception! Just ignore the exception!")
        bag.close()
