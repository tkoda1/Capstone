import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

pwm = GPIO.PWM(12, 50)
pwm.start(0)

def move_servo(angle):
    duty = (angle / 18) + 2  
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)

try:
    while True:
        move_servo(0)    
        time.sleep(2)
        move_servo(180)  
        time.sleep(2)
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()