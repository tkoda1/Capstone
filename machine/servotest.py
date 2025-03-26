# from gpiozero import AngularServo
# from time import sleep

# servo = AngularServo(12, min_angle=0, max_angle=180, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

# def set_angle(angle):
#     servo.angle = angle
#     sleep(1)

# try: 
#     while True: angle = int(input("Enter angle 0-180: "))
#     set_angle(angle)

# except KeyboardInterrupt:
#     print("program stopped by user")

import time
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio

i2c = busio.I2C(SCL, SDA)
pwm = PCA9685(i2c)
pwm.frequency = 60

channel = 0
min_pulse = 150
max_pulse = 600

while True:
    print("Moving to min")
    pwm.channels[channel].duty_cycle = min_pulse
    time.sleep(1)
    
    print("Moving to max")
    pwm.channels[channel].duty_cycle = max_pulse
    time.sleep(1)