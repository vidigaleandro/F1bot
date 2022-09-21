#!/usr/bin/env python
	
import rospy
from ackermann_msgs.msg import AckermannDriveStamped
import RPi.GPIO as gpio
import time
import numpy as np
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

pin26_prevtime = rospy.Time.now()
pin26_time = rospy.Time.now()
pin19_prevtime = rospy.Time.now()
pin19_time = rospy.Time.now()
t = rospy.Time(0).to_sec()


current_time = rospy.Time.now()
last_time = rospy.Time.now()

def callback(data):
    global set_vel
    set_vel = data.drive.speed

def encoder2(pin):
    global pin19_time
    pin19_time = rospy.Time.now()

def encoder1(pin):
    global pin26_prevtime, pin19_prevtime, pin26_counter, pin26_time, t, speed, direction
    #time.sleep(0.005)
    pin26_time =rospy.Time.now()
    
    pin26_counter += 1
    #print(pin26_counter)
    
    #speed = (pin26_time - pin26_prevtime)
    #speed = 1/speed
    if speed > 2000:
    	speed = 2000
    
    #print(t2)
    
    t2 = (pin26_time - pin26_prevtime).to_sec()
    #print (t2)
    t = t + t2
    dist19=abs(pin19_time-pin26_prevtime).to_sec()
    t3 = abs(pin19_time-pin26_prevtime)
     
    #while not gpio.input(19):
    #    time.sleep(0.000001)
    #pin19_time = time.time()
    #print (t)
    
    if pin19_prevtime != pin19_time:
	print("pin26", pin26_time.to_sec())
        print("pin26_prev", pin26_prevtime.to_sec())
        print("pin19_time", pin19_time.to_sec())
    	print("dist19: ", dist19)
    	print("dist_time: ", t2)
    	print("Percentual: ", (dist19/t2)*100)
	if dist19 > 0.80*t2:
	    direction = 1
	else:
	    direction = -1
    #print(direction)
    if t > (0.001):
	    speed=direction*pin26_counter/t
	    print (speed)
            pin26_counter = 0
            t = 0
    pin26_prevtime = pin26_time
    pin19_prevtime = pin19_time

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
gpio.add_event_detect(26, gpio.FALLING, encoder1)
gpio.add_event_detect(19, gpio.RISING, encoder2)
pwm2reg = 0


rospy.Subscriber('Drive', AckermannDriveStamped, callback)



def steering_wheel():
    global speed, pwm2reg, set_vel, dt, last_time
    
    edT = 0                         # Derivative Error
    eprev = 0                       # Previous Error
    eint = 0                        # Integral Error
    u = 0                           # Control Signal

    # PID Constants
    kp = 0.06                          # Proporcional PID Gain
    kd = 0                          # Diferencial PID Gain
    ki = 0.001                          # Integral PID Gain
    
    pub = rospy.Publisher('AcDrive', AckermannDriveStamped, queue_size=1)
    
    pwr = 0
    while not rospy.is_shutdown():

        current_time = rospy.Time.now()
        dt = (current_time - last_time).to_sec()
	
        #print(speed)
        
        if speed > 1999:
	     speed = 0
        
        
        set_vel = 250
        error = (set_vel-speed)             # Calculate Vel Error
        edT = (error-eprev)/dt                  # derivative error calculate
        eint = eint + error*dt                  # integral error calculate
        u = kp*error + kd*edT + ki*eint         # control signal
        eprev = error                           # store previous error
	
	#print(u)
	
        # motor power
	#if u <0:
	#     u=0.05     
	pwr = abs(u)
	

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
	    gpio.output(13, 1)
	   # gpio.output(20, 1)
            # print("Para Tras")

        elif dir == 1:
	    gpio.output(13, 0)
            gpio.output(20, 1)
            #gpio.output(20,0)
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
