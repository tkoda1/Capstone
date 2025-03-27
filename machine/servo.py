import socket
import time
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio

# Initialize PCA9685
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50  

# Servo pulse range in milliseconds
MIN_PULSE = 600  
MAX_PULSE = 2400  

def angle_to_duty(angle):
    pulse_width = MIN_PULSE + (angle / 180.0) * (MAX_PULSE - MIN_PULSE)
    duty_cycle = int(pulse_width * 65535 / 20000)
    return duty_cycle

def dispense_pill(slot, angle=180):
    duty_cycle = angle_to_duty(angle)
    pca.channels[slot].duty_cycle = duty_cycle
    print(f"Moving slot {slot} to {angle} degrees.")
    time.sleep(1)

def reset_servo(slot):
    """ Reset the servo to its neutral position (0 degrees). """
    pca.channels[slot].duty_cycle = angle_to_duty(0)  # Move to 0 degrees
    print(f"Resetting slot {slot} to 0 degrees.")
    time.sleep(1)