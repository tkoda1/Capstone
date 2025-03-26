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

# Bluetooth Server Setup
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
            slot, angle = map(int, message.split(","))

            if 0 <= slot <= 5 and 0 <= angle <= 180:
                dispense_pill(slot, angle)
                client.send(f"Moved slot {slot} to {angle} degrees.".encode('utf-8'))
            else:
                client.send("Slot must be 0-5 and angle must be 0-180.".encode('utf-8'))

        except ValueError:
            client.send("Invalid input format. Send 'slot,angle'.".encode('utf-8'))

except OSError as e:
    print(f"Error: {e}")

finally:
    client.close()
    server.close()

