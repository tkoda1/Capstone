# Referencing GPIO documentation at https://gpiozero.readthedocs.io/en/v1.5.1/recipes.html#servo

# import socket
# from gpiozero import AngularServo
# from time import sleep

# SERVER_ADDRESS = "2C:CF:67:7E:B0:E4"  
# PORT = 1

# servo = AngularServo(18, min_angle=0, max_angle=180, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

# def set_angle(angle):
#     servo.angle = angle
#     sleep(1)

# server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
# server.bind((SERVER_ADDRESS, PORT))
# server.listen(1)

# print(f"Server listening on {SERVER_ADDRESS}:{PORT}...")

# client, addr = server.accept()
# print(f"Connected to {addr}")

# try:
#     while True:
#         data = client.recv(1024)
#         if not data:
#             break
#         message = data.decode('utf-8')
        
#         try:
#             angle = int(message)
#             if 0 <= angle <= 180:
#                 print(f"Setting angle to: {angle}")
#                 set_angle(angle)  
#                 client.send(f"Angle set to {angle}".encode('utf-8'))
#             else:
#                 client.send("Please enter a valid angle between 0 and 180.".encode('utf-8'))
#         except ValueError:
#             client.send("Invalid input. Please send an integer.".encode('utf-8'))
# except OSError as e:
#     pass

# client.close()
# server.close()

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

def dispense_pill(slot, angle=180):
    min_pulse = 1.0  
    max_pulse = 2.0  
    period = 20 

    pulse_width = min_pulse + (angle / 180.0) * (max_pulse - min_pulse)
    
    duty_cycle = int((pulse_width / period) * 65535)

    pca.channels[slot].duty_cycle = 4096 

SERVER_ADDRESS = "2C:CF:67:7E:B0:E4"  
PORT = 1

server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
server.bind((SERVER_ADDRESS, PORT))
server.listen(1)

print(f"Bluetooth Server listening on {SERVER_ADDRESS}:{PORT}...")

client, addr = server.accept()
print(f"Connected to {addr}")

try:
    while True:
        data = client.recv(1024)
        if not data:
            break
        message = data.decode('utf-8')

        try:
            slot = int(message)
            if 0 <= slot <= 5:
                print(f"Received slot: {slot}, moving servo.")
                dispense_pill(slot)
                client.send(f"Moved pill slot {slot}".encode('utf-8'))
            else:
                client.send("Please enter a valid angle between 0 and 5.".encode('utf-8'))

        # try:
        #     angle = int(message)
        #     if 0 <= angle <= 180:
        #         print(f"Received angle: {angle}, moving servo.")
        #         set_angle(angle) 
        #         client.send(f"Angle set to {angle}".encode('utf-8'))
        #     else:
        #         client.send("Please enter a valid angle between 0 and 180.".encode('utf-8'))
        except ValueError:
            client.send("Invalid input. Please send an integer.".encode('utf-8'))
except OSError as e:
    pass

client.close()
server.close()

