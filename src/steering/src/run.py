#!/usr/bin/env python
import rospy
from steering import util
from std_msgs.msg import String
from steering.msg import steer
from smbus2 import SMBus
import RPi.GPIO as gpio
import time
global angle

# Variaveis Globais

pin26_prevtime = time.time()
pin26_counter = 0
pin26_time = time.time()
angle = 0
t = 0
vel = 0


def encoder(pin):
    global pin26_prevtime, pin26_counter, pin26_time, t, vel
    pin26_counter += 1
    pin26_time = time.time()
    # print("pin26:",gpio.input(26),"counter",pin26_counter,"TIME",pin26_time)
    t = t + (pin26_time - pin26_prevtime)
    pin26_prevtime = time.time()
    # print("tempo",t)
    if t > 0.1:
        vel = pin26_counter/t
        print("Velocidade = ", vel)
        pin26_counter = 0
        t = 0


def callback(data):
    global angle
    rospy.loginfo("Angle: %f", data.a)
    angle = data.a


def listener():
    rospy.init_node("Subscriber_Node", anonymous=True)
    rospy.Subscriber('Drive', steer, callback)
    # rospy.spin()


gpio.setwarnings(False)

gpio.setmode(gpio.BCM)
gpio.setup(18, gpio.OUT)

pwm = gpio.PWM(18, 1000)
gpio.setup(17, gpio.OUT)
gpio.setup(27, gpio.OUT)
gpio.setup(22, gpio.OUT)
gpio.setup(26, gpio.IN, pull_up_down=gpio.PUD_DOWN)

pwm.start(1)
gpio.setup(20, gpio.OUT)
pwm2 = gpio.PWM(20, 1000)
gpio.setup(16, gpio.OUT)
pwm2.start(5)

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
pwm2reg = 10


def steering_wheel():
    global vel, pwm2reg
    while not rospy.is_shutdown():
        # Start conversion
        bus.write_i2c_block_data(address, reg_config, config)
        # Wait for conversion
        time.sleep(0.01)
        # Read 16-bit result
        result = bus.read_i2c_block_data(address, reg_conversion, 2)
        # Convert from 2-complement
        value = ((result[0] & 0xFF) << 8) | (result[1] & 0xFF)
        if value & 0x8000 != 0:
            value -= 1 << 16
        # Convert value to voltage
        v = value * 4.096 / 32768
        #print(f'A0: {v} V')
        # Wait a second to start again
        steerangle = angle/44.44+0.525
        error = steerangle-v
        print("Angle", angle)
        print("ANGLE2", steerangle)
        print("Error", error)
        print("V = ", v)
        if error < 0 and abs(error) > 0.02:
            pwm.ChangeDutyCycle(1)
            time.sleep(0.05)
            gpio.output(22, 1)
            gpio.output(17, 1)
            gpio.output(27, 0)
            print("esquerda")

        elif error > 0 and abs(error) > 0.02:
            pwm.ChangeDutyCycle(1)
            time.sleep(0.05)
            gpio.output(22, 1)
            gpio.output(17, 0)
            gpio.output(27, 1)
            print("direita")

        else:
            gpio.output(22, 0)
            # print("Parado")
        set_vel = 250
        error2 = set_vel-vel
        if error2 > 0 and abs(error2) > 10:
            pwm2reg = pwm2reg + 0.1
            print("pwm", pwm2reg)
            if pwm2reg > 20:
                pwm2reg = 20
            pwm2.ChangeDutyCycle(pwm2reg)
            gpio.output(16, 1)
        elif error2 < 0 and abs(error2) > 10:
            pwm2reg = pwm2reg - 0.1
            print("pwmmenos", pwm2reg)
            if pwm2reg < 0.1:
                pwm2reg = 0
            pwm2.ChangeDutyCycle(pwm2reg)
            gpio.output(16, 1)

if __name__ == '__main__':
    try:
        listener()
        steering_wheel()
    except rospy.ROSInterruptException:
        pass
