# # https://chatgpt.com/c/67f3fb13-a568-8002-93b3-3622318d4105
# from gpiozero import OutputDevice
# from hx711 import HX711
# import time

# # Define GPIO pins for HX711
# DT_PIN = 5  # Data pin
# SCK_PIN = 6  # Clock pin

# # Create HX711 instance
# hx = HX711(DT_PIN, SCK_PIN)

# # Tare the scale (zero the load cell)
# hx.tare()

# # Optional: set reference unit for calibration
# # You will need to calibrate the load cell before using it for accurate measurements
# hx.set_reference_unit(1)

# # Function to read the weight
# def read_weight():
#     try:
#         # Read the value from the load cell
#         weight = hx.get_weight(5)  # Average of 5 readings
#         print(f"Weight: {weight} grams")
#         return weight
#     except (KeyboardInterrupt, SystemExit):
#         raise
#     except:
#         print("Error reading weight")

# # Main loop to continuously read weight
# if __name__ == "__main__":
#     try:
#         while True:
#             weight = read_weight()
#             time.sleep(1)  # Adjust delay as needed
#     except KeyboardInterrupt:
#         print("Program interrupted")
#     finally:
#         print("Cleaning up...")
#         hx.power_down()
#         hx.power_up()


# https://chatgpt.com/share/67dca560-2a58-8002-8556-78d4938bd12b

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
    # Remove set_reading_format as it's not supported
    hx.set_reference_unit(calibration_factor)
    hx.reset()
    hx.tare()

def read_weight():
    # Returns weight, make sure to use the right number of readings for averaging
    weight = hx.get_weight(5)
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
