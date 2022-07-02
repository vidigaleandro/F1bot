#!/usr/bin/env python


from visualization_msgs.msg import Marker, MarkerArray
import sys
import numpy as np
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Vector3, Point, Quaternion, Pose
from ackermann_msgs.msg import AckermannDriveStamped
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Header, ColorRGBA
import math
import time
from std_srvs.srv import Empty
from tf.transformations import euler_from_quaternion, quaternion_from_euler

ack_publisher = None

tup  = ([0 , 0],[0 , 0])
Fsen = np.asarray(tup)
yaw = 0
Fobs = [0,0]

linear_speed = 0

markera = Marker()
markerb = Marker()
markerc = Marker()
marker_array = MarkerArray()
markerpath = Marker()


count = 0
linear_speed_med = 1
id = 0

def odom_callback(msg):
    global x, y, roll, pitch, yaw 
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)

def scan_callback(msg):
    global Fobs

    Fobs = Fi(msg)
     


def Fi(data):
    global Fsen
    xa = 0
    ya = 0
    n = 1.5
    d= 0.1
    ran = np.asarray(data.ranges)
      
    for i in range(0,1080,8):
        if ran[i] > 0.01 and ran[i] < 0.9:
            
            xa += n*((ran[i]*math.cos((((i*3/9))*math.pi/180))*2*(d-ran[i]))/(d*ran[i]**4))
            ya += n*((ran[i]*math.sin((((i*3/9))*math.pi/180))*2*(d-ran[i]))/(d*ran[i]**4))
            
    
           
    Fsen[0] = ([-xa,-ya])

    return Fsen[0]



def go_to_goal(x_goal,y_goal):
    global x, y, yaw, Fsum, Fobs, linear_speed, line_point,count,linear_speed_med, marker, line_save,id
 
    markerArray = MarkerArray()
    markera = Marker()
    markera.header.frame_id = "/base_link"
    markerb = Marker()
    markerb.header.frame_id = "/base_link"
    markerc = Marker()
    markerc.header.frame_id = "/base_link"
    ack_msg = AckermannDriveStamped()
    ack_msg.header.stamp = rospy.Time.now()
    ack_msg.header.frame_id = ''
    ack_msg.drive.steering_angle = 0.0
    angular_yaw = 0
    max_steering_angle = rospy.get_param('~max_steering_angle')
    max_speed = rospy.get_param('~max_speed')
    k= 3000
    K_angular = 1
    speed = []

    while not rospy.is_shutdown():

       
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



    
    

        distance = abs(math.sqrt(((x_goal-x) ** 2) + ((y_goal-y) ** 2)))
        qx = (x_goal-x)
        qy = (y_goal-y)
        Fdist = [qx,qy]
        desired_angle_goal_dist = ((math.atan2(qy, qx)))
        
        Fobsmod= abs((math.sqrt(((Fobs[1]) ** 2) + ((Fobs[0]) ** 2)))/1)
        desired_angle_goal_obs=((math.atan2(Fobs[1], Fobs[0])))

    
        
        if yaw<0:
            yaw += 2*math.pi
        
        



        if desired_angle_goal_dist<0:
            desired_angle_goal_dist += 2*math.pi

        if desired_angle_goal_obs<0:
            desired_angle_goal_obs += 2*math.pi



        
        angular_yaw_dist = (desired_angle_goal_dist-yaw)
        
        angular_yaw_obs = (desired_angle_goal_obs)*K_angular
        
  


        

        (xo,yo,zo,wo) = quaternion_from_euler(0.0, 0.0, angular_yaw)
        
        markera.pose.orientation.x = xo
        markera.pose.orientation.y = yo
        markera.pose.orientation.z = zo
        markera.pose.orientation.w = wo

        (xo,yo,zo,wo) = quaternion_from_euler(0.0, 0.0, angular_yaw_dist)
        
        markerb.pose.orientation.x = xo
        markerb.pose.orientation.y = yo
        markerb.pose.orientation.z = zo
        markerb.pose.orientation.w = wo

        (xo,yo,zo,wo) = quaternion_from_euler(0.0, 0.0, angular_yaw_obs)
        
        markerc.pose.orientation.x = xo
        markerc.pose.orientation.y = yo
        markerc.pose.orientation.z = zo
        markerc.pose.orientation.w = wo



        Fdist[0]=(k*math.cos(angular_yaw_dist))
        Fdist[1]=(k*math.sin(angular_yaw_dist))

        Fobs[0]=Fobsmod*math.cos(angular_yaw_obs)
        Fobs[1]=Fobsmod*math.sin(angular_yaw_obs)

        Fsum =  Fdist + Fobs
        #print (Fdist)
        angular_yaw  = ((math.atan2((Fsum[1]), Fsum[0])))

        
        linear_speed = 7/(1+5*abs(angular_yaw))
        #print linear_speed
        if angular_yaw > max_steering_angle:
            angular_yaw = 1*max_steering_angle
        if angular_yaw < (-1) * max_steering_angle:
            angular_yaw = 1*-max_steering_angle

        marker = Marker()
        marker.header.frame_id = "/map"
        marker.type = marker.LINE_STRIP
        marker.action = marker.ADD

        marker.scale.x = 0.2
        marker.scale.y = 0.2
        marker.scale.z = 0.2


       
        marker.pose.orientation.x = 0.0
        marker.pose.orientation.y = 0.0
        marker.pose.orientation.z = 0.0
        marker.pose.orientation.w = 1.0
        
        marker.pose.position.x = 0.0
        marker.pose.position.y = 0.0
        marker.pose.position.z = 0.0
        

        marker.lifetime = rospy.Duration.from_sec(0)

        
        line_point = Point()
        line_point.x = x
        line_point.y = y
        line_point.z = 1.0

        if count == 0:
            line_save = line_point
            marker.points = []
            #marker.points.append(line_point)

        speed.append(linear_speed)
        count += 1
        #print(count)
        #print(marker.points)
        if count == 20:
            marker.points.append(line_save)
            marker.points.append(line_point)

            markerArray.markers.append(marker)
            linear_speed_med = (sum(speed))/20
            #print(linear_speed_med)
            speed = []
            for m in markerArray.markers:
                m.id = id
                id += 1  
                if id == 2000:
                    id = 0   
                #print id

            marker.color.a = 0.5
            marker.color.g = linear_speed_med/7
            marker.color.r = 1-(linear_speed_med/7)
            publisher.publish(markerArray)

            count = 0
            
  
        


        ack_msg.drive.speed = linear_speed
        ack_msg.drive.steering_angle = angular_yaw

        ack_publisher.publish(ack_msg)
        publishera.publish(markera)
        publisherb.publish(markerb)
        publisherc.publish(markerc)
        

        #pub_line_min_dist.publish(marker)

        #print 'x=', x, 'y=',y, "yaw=",yaw, "desired=", angular_yaw


        time.sleep(0.01)
        if (distance <1.5):
            break
    ack_msg.drive.speed = 0.0
    ack_publisher.publish(ack_msg)
            
    
    
    
if __name__=='__main__':
    try:

        rospy.init_node('robot_motion_pose', anonymous=True)
        odom_sub = rospy.Subscriber('/odom', Odometry, odom_callback)
        publishera = rospy.Publisher('Result', Marker, queue_size=1)
        publisherb = rospy.Publisher('Distancia', Marker, queue_size=1)
        publisherc = rospy.Publisher('Parede', Marker, queue_size=1)
        scan_sub = rospy.Subscriber('scan', LaserScan, scan_callback) 
        drive_topic = rospy.get_param('~auto_drive_topic') 
        ack_publisher = rospy.Publisher(drive_topic, AckermannDriveStamped, queue_size=1)
        pub_line_min_dist = rospy.Publisher('~line_min_dist', Marker, queue_size=1)
        publisher = rospy.Publisher('visualization_marker_array', MarkerArray, queue_size=1)
        
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

        go_to_goal(9.5,0)
        print("Next point")
        go_to_goal(9.5,8.5)
        print("Next point")
        go_to_goal(-13.8,8)
        print("Next point")
        go_to_goal(-13.8,0)
        print("Next point")
        go_to_goal(9.5,0)
        go_to_goal(9.5,8.5)
        print("Next point")
        go_to_goal(-13.8,8)
        print("Next point")
        go_to_goal(-13.8,0)
        print("Next point")
        go_to_goal(9.5,0)        
        go_to_goal(9.5,8.5)
        print("Next point")
        go_to_goal(-13.8,8)
        print("Next point")
        go_to_goal(-13.8,0)
        print("Next point") 
        go_to_goal(9.5,0)    
        go_to_goal(9.5,8.5)
        print("Next point")
        go_to_goal(-13.8,8)
        print("Next point")
        go_to_goal(-13.8,0)
        print("Next point")
        go_to_goal(9.5,0)

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
