#!/usr/bin/env python

import rospy
from ackermann_msgs.msg import AckermannDriveStamped
import RPi.GPIO as gpio
import time
import numpy as np
from statistics import mode, median
global set_vel

# Variaveis Globais
dt = 0
pin26_fallingtime = 0
pin26_counter = 0
speed = 0
set_vel = 0
direction = 1
#t = 0



rospy.init_node("Aceleration_Drive", anonymous=True)

dist = 0
pin26_prevtime = 0
pin26_time = 0
pin26_duration = 0
pin19_prevtime = 0
pin19_time = 0
pin19_duration = 0
speed_ant = 0
t = rospy.Time(0).to_sec()
speed_med = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
dist_med = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
current_time = rospy.Time.now()
last_time = rospy.Time.now()
dir = 1 
dir_med = [0,0,0,0,0,0,0,0,0,0,0]
pin19_ant = 0
def callback(data):
    global set_vel
    set_vel = data.drive.speed

#GPIO CONFIG

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(26, gpio.IN, pull_up_down=gpio.PUD_DOWN)  # GPIO - INPUT ENCONDER 1
gpio.setup(19, gpio.IN, pull_up_down=gpio.PUD_DOWN)  # GPIO - INPUT ENCONDER 2
gpio.setup(16, gpio.OUT)			     # GPIO - OUTPUT PWM 
pwm2 = gpio.PWM(16, 1000)
gpio.setup(13, gpio.OUT)		#GPIO - OUTPUT TO BACK
gpio.setup(20, gpio.OUT)		#GPIO - OUTPUT TO FOWARD
pwm2.start(0)


pwm2reg = 0


rospy.Subscriber('Drive', AckermannDriveStamped, callback)



def steering_wheel():
    global speed, pwm2reg, set_vel, dt, last_time, pin26_duration,pin19_ant, pin19_time, pin26_time, speed_ant,dist, speed_med, dist_med, dir, dir_med
    dt_sum = 0
    count = 0
    edT = 0                         # Derivative Error
    eprev = 0                       # Previous Error
    eint = 0                        # Integral Error
    u = 0                           # Control Signal
    teste = 0
    # PID Constants
    kp = 3                          # Proporcional PID Gain
    kd = 0                             # Diferencial PID Gain
    ki = 0.0005                          # Integral PID Gain
    vel = 0
    pub = rospy.Publisher('AcDrive', AckermannDriveStamped, queue_size=1)
    vel_time_ant = rospy.Time(0).to_sec()
    pwr = 0
    vel_med = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    vel_ant = 10
    while not rospy.is_shutdown():
	pin19 = gpio.input(19)
        pin26 = gpio.input(26)
	
	if pin19_ant != pin19 :
	    vel_time = rospy.Time.now().to_sec()
            vel = 0.0017/(vel_time - vel_time_ant)
            vel_time_ant = vel_time
	    
	pin19_ant = pin19
	dir_med.append(dir)
        dir_med.pop(0)
	real_dir = median(dir_med)

        current_time = rospy.Time.now()
        dt = (current_time - last_time).to_sec()
	#print(dt)
	dt_sum += dt
	#print("velocidade!", vel)
	#print("DT_SUM", dt_sum)
	if dt_sum >= 0.05:
	    teste = count
	    count = 0
	    dt_sum = 0
        
	#print("velocidade", teste)
        
        if speed > 10:
	     speed = 10
        
        
        #set_vel = 3
	
        
	if vel != vel_ant:
            vel_med.append(vel)
	    vel_med.pop(0)
	    real_vel = median(vel_med)
	    error = (set_vel-real_vel)             # Calculate Vel Error
            print("error", error)
            edT = (error-eprev)/dt                  # derivative error calculate
            eint = eint + error*dt                  # integral error calculate
            u = kp*error + kd*edT + ki*eint         # control signal
	    print("u", u)
            eprev = error                           # store previous error
	    #print (vel_med)
	    #print (real_dir)
	    print("SPEEEEEEEEEEDDDD:", real_vel)
	    	
	vel_ant= vel	
	
        
	
	#print(u)
	
        # motor power
	#if u <0:
	#     u=0.05     
	pwr = abs(u)
	#print("pwr:",pwr)

        if(pwr > 100):
            pwr = 100

        #print(speed)

        # motor direction
        dir = 1
        if (u < 0):
            dir = -1

        pwm2.ChangeDutyCycle(pwr) # Set Pwm Control

        # Set PWN Output
        if dir == -1:
            gpio.output(20, 0)
	    gpio.output(13, 0)
	   # gpio.output(20, 1)
            # print("Para Tras")

        else:
	    gpio.output(13, 0)
            gpio.output(20, 1)
            #gpio.output(20,0)
            #print("Para Frente")
	
	AcMsg = AckermannDriveStamped()
	AcMsg.drive.speed = real_vel
	AcMsg.drive.jerk = set_vel
	pub.publish(AcMsg)

        
        last_time = current_time

if __name__ == '__main__':
    try:
        steering_wheel()
    except rospy.ROSInterruptException:
        rospy.logerr("ROS Interrupt Exception! Just ignore the exception!")
