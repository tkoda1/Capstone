# https://www.youtube.com/watch?v=FdFXlTdpueQ

import RPi.GPIO as GPIO
from hx711 import HX711

GPIO.setmode(GPIO.BCM)

hx = HX711(dout_pin=6, pd_sck_pin=5)

hx.zero()

while True:
    reading = hx.get_raw_data_mean()
    print(reading)

# # https://chatgpt.com/share/67dca560-2a58-8002-8556-78d4938bd12b

# import RPi.GPIO as GPIO
# from hx711 import HX711
# import time

# DOUT = 5
# SCK = 6 

# hx = HX711(DOUT, SCK)

# calibration_factor = 2280  # You will need to calibrate your load cell and adjust this value

# def setup():
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setwarnings(False)
#     hx.set_reading_format("MSB", "MSB")
#     hx.set_reference_unit(calibration_factor)
#     hx.reset()
#     hx.tare()

# def read_weight():
#     weight = hx.get_weight(5)
#     return weight

# if __name__ == "__main__":
#     setup()
#     print('Testing load cell...')
#     weight = read_weight()
#     print('Read weight {weight} grams')
#     time.sleep(1)
#     GPIO.cleanup()
#     time.sleep(1)
#     print('Finished testing load cell')