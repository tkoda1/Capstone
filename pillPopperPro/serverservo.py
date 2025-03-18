# Referencing GPIO documentation at https://gpiozero.readthedocs.io/en/v1.5.1/recipes.html#servo

import socket
from gpiozero import AngularServo
from time import sleep

SERVER_ADDRESS = "2C:CF:67:7E:B0:E4"  
PORT = 1

servo = AngularServo(12, min_angle=0, max_angle=180, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

def set_angle(angle):
    servo.angle = angle
    sleep(1)

server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
server.bind((SERVER_ADDRESS, PORT))
server.listen(1)

print(f"Server listening on {SERVER_ADDRESS}:{PORT}...")

client, addr = server.accept()
print(f"Connected to {addr}")

try:
    while True:
        data = client.recv(1024)
        if not data:
            break
        message = data.decode('utf-8')
        
        try:
            angle = int(message)
            if 0 <= angle <= 180:
                print(f"Setting angle to: {angle}")
                set_angle(angle)  
                client.send(f"Angle set to {angle}".encode('utf-8'))
            else:
                client.send("Please enter a valid angle between 0 and 180.".encode('utf-8'))
        except ValueError:
            client.send("Invalid input. Please send an integer.".encode('utf-8'))
except OSError as e:
    pass

client.close()
server.close()
