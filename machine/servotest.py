from gpiozero import Servo
from time import sleep

servo = Servo(12)

while True:
    servo.min()  
    sleep(2)
    servo.max() 
    sleep(2)