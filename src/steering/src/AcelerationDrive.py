#!/usr/bin/env python
	
import rospy
from ackermann_msgs.msg import AckermannDriveStamped
import RPi.GPIO as gpio
import time
import numpy as np
global set_vel

# Variaveis Globais
dt = 0
pin26_prevtime = time.time()
pin26_counter = 0
pin26_time = time.time()
speed = 0
set_vel = 0
t = 0

rospy.init_node("Aceleration_Drive", anonymous=True)

current_time = rospy.Time.now()
last_time = rospy.Time.now()

def callback(data):
    global set_vel
    set_vel = data.drive.speed

def encoder(pin):
    global pin26_prevtime, pin26_counter, pin26_time, t, speed

    pin26_counter += 1
    #print(pin26_counter)
    pin26_time = time.time()
    #speed = (pin26_time - pin26_prevtime)
    #speed = 1/speed
    if speed > 2000:
    	speed = 2000
    
	#print(t2)
    t2 = (pin26_time - pin26_prevtime)
    t = t + t2
    pin26_prevtime = time.time()

    if t > 0.001:
        speed=pin26_counter/t
	#print (speed)
        pin26_counter = 0
        t = 0

rospy.Subscriber('Drive', AckermannDriveStamped, callback)

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(26, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(20, gpio.OUT)
pwm2 = gpio.PWM(20, 1000)
gpio.setup(16, gpio.OUT)
pwm2.start(0)

gpio.add_event_detect(26, gpio.BOTH, encoder)
pwm2reg = 0

def steering_wheel():
    global speed, pwm2reg, set_vel, dt, last_time
    
    edT = 0                         # Derivative Error
    eprev = 0                       # Previous Error
    eint = 0                        # Integral Error
    u = 0                           # Control Signal

    # PID Constants
    kp = 0.2                          # Proporcional PID Gain
    kd = 0.0001                          # Diferencial PID Gain
    ki = 0.0002                          # Integral PID Gain
    
    pub = rospy.Publisher('AcDrive', AckermannDriveStamped, queue_size=1)
    
    pwr = 0
    while not rospy.is_shutdown():

        current_time = rospy.Time.now()
        dt = (current_time - last_time).to_sec()
	
        #print(speed)
        
        if speed > 1999:
	     speed = 0
        
        
        #set_vel = 100
        error = (set_vel-speed)             # Calculate Vel Error
        edT = (error-eprev)/dt                  # derivative error calculate
        eint = eint + error*dt                  # integral error calculate
        u = kp*error + kd*edT + ki*eint         # control signal
        eprev = error                           # store previous error
	
	#print(u)
	
        # motor power
	if u <0:
	     u=0.05     
	pwr = abs(u)
	

        if(pwr > 100):
            pwr = 100

        print(speed)

        # motor direction
        dir = 1
        if (u < 0):
            dir = -1

        pwm2.ChangeDutyCycle(pwr) # Set Pwm Control

        # Set PWN Output
        if dir == -1:
            gpio.output(16, 0)
            # print("Para Tras")

        elif dir == 1:
            gpio.output(16, 1)
            # print("Para Frente")
	
	AcMsg = AckermannDriveStamped()
	AcMsg.drive.speed = speed
	AcMsg.drive.jerk = set_vel
	pub.publish(AcMsg)

        
        last_time = current_time

if __name__ == '__main__':
    try:
        steering_wheel()
    except rospy.ROSInterruptException:
        rospy.logerr("ROS Interrupt Exception! Just ignore the exception!")
