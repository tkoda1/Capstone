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

# import time
# from adafruit_pca9685 import PCA9685
# from board import SCL, SDA
# import busio

# i2c = busio.I2C(SCL, SDA)

# print("staring)")
# pwm = PCA9685(i2c)
# pwm.frequency = 60
# channel = 0
# min_pulze = 150
# max_pulse = 600
# pwm.channels[channel].duty_cycle = max_pulse
# time.sleep(1)
# print("done")

import time
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio

# Initialize I2C and PCA9685
i2c = busio.I2C(SCL, SDA)
pwm = PCA9685(i2c)
pwm.frequency = 50  # MG996R expects ~50Hz

# Adjusted for MG996R
min_pulse = 600     # μs
max_pulse = 2400    # μs

servo_channel = 0

def angle_to_duty(angle):
    pulse_width = min_pulse + (angle / 180.0) * (max_pulse - min_pulse)
    duty_cycle = int(pulse_width * 65535 / 20000)  # 20ms = 1 period at 50Hz
    return duty_cycle

try:
    while True:
        angle = input("Enter angle 10–170 (or 'q' to quit): ")
        if angle.lower() == 'q':
            break
        try:
            angle = float(angle)
            if 10 <= angle <= 170:
                duty = angle_to_duty(angle)
                pwm.channels[servo_channel].duty_cycle = duty
                print(f"Moving servo to {angle} degrees")
                time.sleep(1)
            else:
                print("Try staying between 10 and 170 degrees.")
        except ValueError:
            print("Enter a valid number.")

except KeyboardInterrupt:
    print("Program stopped.")

finally:
    pwm.deinit()