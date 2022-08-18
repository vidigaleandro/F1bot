#!/usr/bin/env python


from tf.transformations import euler_from_quaternion
import tf
import os
import rospy
import numpy as np
import math
from steering import util
from steering.msg import steer
from std_msgs.msg import String
from ackermann_msgs.msg import AckermannDriveStamped, AckermannDrive
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
from sensor_msgs.msg import Imu
from smbus2 import SMBus
import RPi.GPIO as gpio
import time
global angle
global set_vel
global PAng
global yaww
# Variaveis Globais
dt = 0
print(dt)
pin26_prevtime = time.time()
pin26_counter = 0
pin26_time = time.time()
angle = 0
t = 0
vel = 0
set_vel = 0
PAng = rospy.Publisher('Drive', steer, queue_size=10)
yaww = 0
yaw = 0
orientation_list = None
x = 0
y = 0
tint = 0
velo = [0, 0, 0, 0, 0]
x_vel = 0
y_vel = 0
roll=0
pitch=0

odom_pub = rospy.Publisher("odom", Odometry, queue_size=1) 
odom_broadcaster = tf.TransformBroadcaster()
rospy.init_node("Subscriber_Node", anonymous=True)
#rospy.init_node('odometrys_publisher', anonymous=True)
current_time = rospy.Time.now()
last_time = rospy.Time.now()




current_time = rospy.Time.now()
last_time = rospy.Time.now()


def encoder(pin):
    global pin26_prevtime, pin26_counter, pin26_time, t, vel
#    k = 450
    pin26_counter += 1
    pin26_time = time.time()
    # print("pin26:",gpio.input(26),"counter",pin26_counter,"TIME",pin26_time)
    t2 = (pin26_time - pin26_prevtime)
    t = t + t2
    pin26_prevtime = time.time()
#    vel = t2*k
#    print("velocidade atual em m/s",vel)
#    print("tempo dif",t2)
    if t > 0.01:
        vel = pin26_counter/t
#        print("Velocidade = ", vel)
        pin26_counter = 0
        t = 0


def callback(data):
    global angle, set_vel, PAng
    drive_msg = data
    angle = data.drive.steering_angle
    set_vel = data.drive.speed
    PAng = rospy.Publisher('Drive', steer, queue_size=1)
    rate = rospy.Rate(10)
    #print("ANGULO TESTE",angle)
    # print("=====================================================")


def callback2(data):
    global yaw, orientation_list, roll, pitch
    orientation_q = data.orientation
    orientation_list = [orientation_q.x, orientation_q.y,
                        orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion(orientation_list)
    print yaw



def listener():
    
    rospy.Subscriber('Drive', AckermannDriveStamped, callback)
    rospy.Subscriber('/imu/data', Imu, callback2)


def publisher():
    global x,y,yaw,x_vel,y_vel
    #rospy.Publisher("Odom", Odometry, queue_size=1)
    # rospy.spin()
    while not rospy.is_shutdown():
    	odom_quat = tf.transformations.quaternion_from_euler(0, 0, yaw)
    	odom_broadcaster.sendTransform(
       		(x, y, 0.),
       		odom_quat,
       	 	current_time,
       	 	"base_link",
       	 	"odom"
    	)
    	odom = Odometry()
    	odom.header.stamp = rospy.Time.now()
    	odom.header.frame_id = "odom"

    	odom.pose.pose = Pose(Point(x, y, 0.), Quaternion(*odom_quat))
    	odom.child_frame_id = "base_link"
    	odom.twist.twist = Twist(Vector3(x_vel, y_vel, 0), Vector3(0, 0, 0))
    	odom_pub.publish(odom)



gpio.setwarnings(False)

gpio.setmode(gpio.BCM)
gpio.setup(18, gpio.OUT)

pwm = gpio.PWM(18, 250)
gpio.setup(17, gpio.OUT)
gpio.setup(27, gpio.OUT)
gpio.setup(22, gpio.OUT)
gpio.setup(26, gpio.IN, pull_up_down=gpio.PUD_DOWN)

pwm.start(0)
gpio.setup(20, gpio.OUT)
pwm2 = gpio.PWM(20, 1000)
gpio.setup(16, gpio.OUT)
pwm2.start(0)

# RPi Channel 1
channel = 1
# ADS1115 address and registers
address = 0x48
reg_config = 0x01
reg_conversion = 0x00

bus = SMBus(channel)

# Config value:
# - Single conversion
# - A0 input
# - 4.096V reference
config = [0xC2, 0xB3]

#angle = 0.2
Pi = 50
gpio.add_event_detect(26, gpio.BOTH, encoder)
pwm2reg = 0

 
def steering_wheel():
    global vel, pwm2reg, set_vel, PAng, angle, yaww, orientation_list, yaw, x, y, dt, tint, last_time,roll, pitch
    while not rospy.is_shutdown():
        #current_time = rospy.Time.now()
        #dt = (current_time - last_time).to_sec()
	# Start conversion
        bus.write_i2c_block_data(address, reg_config, config)
        # Wait for conversion
        # time.sleep(0.02)
        # Read 16-bit result
        result = bus.read_i2c_block_data(address, reg_conversion, 2)
        # Convert from 2-complement
        value = ((result[0] & 0xFF) << 8) | (result[1] & 0xFF)
        if value & 0x8000 != 0:
            value -= 1 << 16
        # Convert value to voltage
        v = value * 4.096 / 32768
	
        print("====================================================")
        print("YAW: ", yaw)
        print("====================================================")
        print("Orientantion List: ", orientation_list)
        print("====================================================")
        print('v  Valor de tensao: ', v)
        print("====================================================")
        # Wait a second to start again
        angle = angle*1.8  # to keyboard
        #angle = (angle*180)/math.pi #to auto.py
        print("Angulo setado antes: ", angle)
        print("====================================================")
        steerangle = angle/44.44+0.555
        error = steerangle-v
        Act_angle = steer()
        Act_angle.a = ((v-0.555)*44.44)
        print("Angulo Atual: ", (Act_angle.a*math.pi)/(180*1.8))
        print("====================================================")
        # PAng.publish(Act_angle)
        print("Angulo Setado: ", (angle*math.pi)/180)
        print("====================================================")

        os.system('clear')
        #print("ANGLE2", steerangle)
        #print("Error", error)
        #print("V = ", v)
        if error < 0 and abs(error) > 0.0060:
            pwm.ChangeDutyCycle(3)
            # time.sleep(0.05)
            gpio.output(22, 1)
            gpio.output(17, 1)
            gpio.output(27, 0)
 #           print("esquerda")

        elif error > 0 and abs(error) > 0.0060:
            pwm.ChangeDutyCycle(3)
            # time.sleep(0.05)
            gpio.output(22, 1)
            gpio.output(17, 0)
            gpio.output(27, 1)
 #           print("direita")

        else:
            gpio.output(22, 0)
            # print("Parado")
        #set_vel = 250
        vel = vel/525
        error2 = 5.25*(set_vel-vel)
        #print("velocidade setada", set_vel)
        #print("erro na velocidade", error2)
	#error2 = 0
        if error2 > 0 and abs(error2) > 0:
            pwm2reg = pwm2reg + 0.05
  #          print("pwm", pwm2reg)
            if pwm2reg > 20:
                pwm2reg = 20
            pwm2.ChangeDutyCycle(pwm2reg)
            gpio.output(16, 1)
        elif error2 < 0 and abs(error2) > 0:
            pwm2reg = pwm2reg - 0.05
   #         print("pwmmenos", pwm2reg)
            if pwm2reg < 0.11:
                pwm2reg = 0.0
            pwm2.ChangeDutyCycle(pwm2reg)
            gpio.output(16, 1)
        tint += 1
        if tint == 1:
            time_int = time.time()
        if tint == 2:
            time_int2 = time.time()
            dt = time_int2 - time_int
            tint = 0

        velo.append(vel)
        vm = np.mean(velo)
        velo.pop(0)

        print("VEL 1: ", velo)
        x_vel = vel * math.cos(yaw)
        print("Velocidade em X: ", x_vel)
        print("====================================================")
        print("cos", math.cos(yaw))
        print("SEN", math.sin(yaw))
        y_vel = vel * math.sin(yaw)
        print("Velocidade em Y: ", y_vel)
        print("====================================================")
        if vel < 5 * vm and vel > vm/5:
            x = x + 1.15*(x_vel * dt)
            y = y + 1.15*(y_vel * dt)
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
    	odom = Odometry()
    	odom.header.stamp = rospy.Time.now()
    	odom.header.frame_id = "odom"

  	odom.pose.pose = Pose(Point(x, y, 0.), Quaternion(*odom_quat))
    	odom.child_frame_id = "base_link"
    	odom.twist.twist = Twist(Vector3(x_vel, y_vel, 0), Vector3(0, 0, 0))
    	odom_pub.publish(odom)



        
        #last_time = current_time
if __name__ == '__main__':
    try:
        listener()
        steering_wheel()
#	publisher()
	#odom_pub.publish(odom)
    except rospy.ROSInterruptException:
    	rospy.logerr("ROS Interrupt Exception! Just ignore the exception!")
    #  pass
