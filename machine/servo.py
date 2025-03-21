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

def dispense_pill(slot):
    pca.channels[slot].duty_cycle = 8191
    time.sleep(1)