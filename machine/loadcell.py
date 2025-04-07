import RPi.GPIO as GPIO
from hx711 import HX711
import time

DOUT = 5
SCK = 6 

hx = HX711(DOUT, SCK)

calibration_factor = 2280  # You will need to calibrate your load cell and adjust this value

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # Reset the HX711
    hx.reset()
    
    # Read a few times to reset the scale (this is equivalent to taring it)
    print("Taring the load cell...")
    for _ in range(10):  # You can adjust the number of readings for taring
        hx.read()  # Using `read()` method to simulate taring
        time.sleep(0.1)  # Small delay to allow for stable readings

def read_weight():
    # Returns weight, make sure to use the right number of readings for averaging
    weight = hx.read()
    hx.power_down()
    hx.power_up()
    return weight

if __name__ == "__main__":
    setup()
    print('Testing load cell...')
    weight = read_weight()
    print(f'Read weight {weight} grams')  # Corrected the print format
    time.sleep(1)
    GPIO.cleanup()
    time.sleep(1)
    print('Finished testing load cell')