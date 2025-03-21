# Referencing GPIO documentation at https://gpiozero.readthedocs.io/en/v1.5.1/recipes.html#servo

import socket
import time
from adafruit_pca9685 import PCA9685
from digitalio import DigitalInOut
from board import SCL, SDA
import busio

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50  

SERVO_CHANNEL = 0  

def dispense_pill(slot):
    """Convert angle (0-180) to PCA9685 PWM signal and move the servo."""
    min_pulse = 0.5  
    max_pulse = 2.5
    angle = 180

    pulse_width = min_pulse + (angle / 180) * (max_pulse - min_pulse)
    duty = int(pulse_width*65535 /20)
    pca.channels[slot].duty_cycle = int(410 / 4095 * 65535)
    time.sleep(1)  # change this

# def set_angle(angle):
#     """Convert angle (0-180) to PCA9685 PWM signal and move the servo."""
#     min_pulse = 0.5  
#     max_pulse = 2.5

#     pulse_width = min_pulse + (angle / 180) * (max_pulse - min_pulse)
#     duty = int(pulse_width*65535 /20)
#     pca.channels[SERVO_CHANNEL].duty_cycle = duty
#     time.sleep(1)  


for x in range(0,5):
    print(f"Received slot: {x}, moving servo.")
    dispense_pill(x)
    print('Finished dispensing pill')
