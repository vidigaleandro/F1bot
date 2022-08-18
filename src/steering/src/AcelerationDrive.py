#!/usr/bin/env python

import rospy
from ackermann_msgs.msg import AckermannDriveStamped
import RPi.GPIO as gpio
import time

global set_vel

# Variaveis Globais
dt = 0
pin26_prevtime = time.time()
pin26_counter = 0
pin26_time = time.time()
vel = 0
set_vel = 0


rospy.init_node("Aceleration_Drive", anonymous=True)

current_time = rospy.Time.now()
last_time = rospy.Time.now()

def callback(data):
    global set_vel
    set_vel = data.drive.speed

def encoder(pin):
    global pin26_prevtime, pin26_counter, pin26_time, t, vel

    pin26_counter += 1
    pin26_time = time.time()
    t2 = (pin26_time - pin26_prevtime)
    t = t + t2
    pin26_prevtime = time.time()

    if t > 0.01:
        vel = pin26_counter/t
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
    global vel, pwm2reg, set_vel, dt, last_time
    edT = 0                         # Derivative Error
    eprev = 0                       # Previous Error
    eint = 0                        # Integral Error
    u = 0                           # Control Signal

    # PID Constants
    kp = 5.25                       # Proporcional PID Gain
    kd = 1                          # Diferencial PID Gain
    ki = 0                          # Integral PID Gain

    while not rospy.is_shutdown():

        current_time = rospy.Time.now()
        dt = (current_time - last_time).to_sec()

        vel = vel/525

        set_vel = 1
        error = (set_vel-vel)                   # Calculate Vel Error
        edT = (error-eprev)/dt                  # derivative error calculate
        eint = eint + error*dt                  # integral error calculate
        u = kp*error + kd*edT + ki*eint         # control signal
        eprev = error                           # store previous error

        # motor power
        pwr = abs(u)

        if(pwr > 20):
            pwr = 20

        # motor direction
        dir = 1
        if (u < 0):
            dir = -1

        pwm2.ChangeDutyCycle(pwr) # Set Pwm Control

        # Set PWN Output
        if dir == -1:
            gpio.output(16, 0)
            # print("Para Trás")

        elif dir == 1:
            gpio.output(16, 1)
            # print("Para Frente")

        last_time = current_time

if __name__ == '__main__':
    try:
        steering_wheel()
    except rospy.ROSInterruptException:
        rospy.logerr("ROS Interrupt Exception! Just ignore the exception!")
