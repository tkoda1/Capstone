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

print("staring)")
pwm = PCA9685()
pwm.set_pwm_freq(60)
channel = 0
min_pulze = 150
max_pulse = 600
pwm.set_pwm(channel, 0, max_pulse)
time.sleep(1)
print("done")