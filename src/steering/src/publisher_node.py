#!/usr/bin/env python
import rospy
from steering import util
from std_msgs.msg import String
from steering.msg import steer

def callback():
   pub = rospy.Publisher('Drive', steer, queue_size=10)
   rospy.init_node('steer_node', anonymous = True)
   rate = rospy.Rate(1)
   rospy.loginfo("Started")
   while not rospy.is_shutdown():
      msg = steer()
      msg.a =0
      pub.publish(msg)
      rate.sleep()

if __name__ == '__main__':
   try:
      callback()
   except rospy.ROSInterruptException:
      pass


