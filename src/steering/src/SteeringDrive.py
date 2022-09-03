#!/usr/bin/env python

import rospy
import math
from ackermann_msgs.msg import AckermannDriveStamped
from smbus2 import SMBus
import RPi.GPIO as gpio

# Intializate Node

rospy.init_node("SteeringDrive", anonymous=True)

# Global Variables
angle = 0
current_time = rospy.Time.now()
last_time = rospy.Time.now()

# Functions

def callback(data):
    global angle
    drive_msg = data
    angle = data.drive.steering_angle

# Initializate Subscriber
rospy.Subscriber('Drive', AckermannDriveStamped, callback)



# GPIO Setup
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)   #Set mode BCM
gpio.setup(18, gpio.OUT) #Output to PWM 
pwm = gpio.PWM(18, 250)  #SET PWM OUT(PIN,FREQ)
gpio.setup(17, gpio.OUT) #Output to Left  Direction
gpio.setup(27, gpio.OUT) #Output to Right Direction
gpio.setup(22, gpio.OUT) #Lock/Unlock Output
pwm.start(0)

# ADS1115 Setup Analogic/Digital Conversor
channel = 1  # RPi Channel 1
address = 0x48  # ADS1115 address and registers
reg_config = 0x01
reg_conversion = 0x00
bus = SMBus(channel)
config = [0xC2, 0xB3] # Config value: Single conversion;A0 input;4.096V reference

def steering_wheel():
    global angle, last_time
    edT = 0                         # Derivative Error
    eprev = 0                       # Previous Error
    eint = 0                        # Integral Error
    u = 0                           # Control Signal

    # PID Constants
    kp = 100                          # Proporcional PID Gain
    kd = 0.1                          # Diferencial PID Gain
    ki = 1                            # Integral PID Gain

    maxangle = 0.15                   # Max angle RAD
    while not rospy.is_shutdown():
        current_time = rospy.Time.now()             #Time for delta T
        dt = (current_time - last_time).to_sec()    #Calculate delta T

        # Start conversion Angle
        bus.write_i2c_block_data(address, reg_config, config)
        result = bus.read_i2c_block_data(
            address, reg_conversion, 2)  # Read 16-bit result
        value = ((result[0] & 0xFF) << 8) | (
            result[1] & 0xFF)  # Convert from 2-complement
        if value & 0x8000 != 0:
            value -= 1 << 16
        v = value * 4.096 / 32768  # Convert value to voltage

        print("====================================================")
        print('v  Valor de tensao: ', v)
        print("====================================================")

        # Wait a second to start again
        #angle = angle*1.8  # to keyboard
	#angle= 0                 # in radians
        print("====================================================")
        print('Angle: ', angle)
        print("====================================================")

	if angle > maxangle:
            angle = maxangle
	if angle < -maxangle:
            angle = -maxangle
        #if angle > maxangle:
        #    angle = maxangle
        #if angle < -maxangle:
        #    angle = -maxangle

        print("Angulo setado antes: ", angle)
        print("====================================================")

        
        steerangle = ((angle*180)/math.pi)/44.44+1.65  # SET ANGLE

        # Control Calculate
        error = steerangle-v                    # error Calculate
        edT = (error-eprev)/dt                  # derivative error calculate
        eint = eint + error*dt                  # integral error calculate
        u = kp*error + kd*edT + ki*eint         # control signal
        eprev = error                           # store previous error

        print("====================================================")
        print('Error: ', error)
        print("====================================================")

        print("====================================================")
        print('Steering Angle: ', steerangle)
        print("====================================================")



        # motor power
        pwr = abs(u)

        # TODO adjust the error

        if(pwr > 100):
            pwr = 100

        # motor direction
        dir = 1
        if (u < 0):
            dir = -1

        pwm.ChangeDutyCycle(pwr)  # Set Pwm Control

        # Set PWN Output
        if dir == -1:
            gpio.output(22, 1)
            gpio.output(17, 1)
            gpio.output(27, 0)
            # print("esquerda")

        elif dir == 1:
            gpio.output(22, 1)
            gpio.output(17, 0)
            gpio.output(27, 1)
            # print("direita")

        else:
            gpio.output(22, 0)
            # print("Parado")

        last_time = current_time


if __name__ == '__main__':
    try:
        steering_wheel()

    except rospy.ROSInterruptException:
        rospy.logerr("ROS Interrupt Exception! Just ignore the exception!")
	angle = 0
        gpio.output(22,0)
