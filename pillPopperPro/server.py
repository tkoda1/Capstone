# source to see if bluetooth is working: https://www.youtube.com/watch?v=8pMaR-WUc6U

import socket
import RPi.GPIO as GPIO
import time

SERVER_ADDRESS = "2C:CF:67:7E:B0:E4"  # Replace with Raspberry Pi's Bluetooth MAC
PORT = 1

GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT) 
pwm = GPIO.PWM(18, 50)  
pwm.start(0)  


server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
server.bind((SERVER_ADDRESS, PORT))
server.listen(PORT)

client, addr = server.accept()

def set_servo_position(angle):
    duty = (angle / 18) + 2 
    GPIO.output(18, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(18, False)
    pwm.ChangeDutyCycle(0)

# try:
#     while True:
#         data = client.recv(1024)
#         if not data:
#             break
#         print(f"Message: {data.decode('utf-8')}")
#         message = input("Enter Message: ")
#         client.send(message.encode("utf-8"))
# except OSError as e:
#     pass

# client.close()
# server.close()

try:
    while True:
        data = client.recv(1024)
        if not data:
            break
        message = data.decode('utf-8')
        print(f"Received message: {message}")

        if message.lower() == "dispense":
            set_servo_position(180)  
            client.send(b"Dispensing... Servo moved to 180 degrees.")
        else:
            client.send(b"Invalid command. Please send 'dispense'.")
        
except OSError as e:
    pass

client.close()
server.close()
GPIO.cleanup()