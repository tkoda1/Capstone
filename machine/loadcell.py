# https://pypi.org/project/hx711/

from hx711 import HX711

try:
    hx711 = HX711(
        dout_pin=5,
        pd_sck_pin=6,
        channel='A',
        gain=64
    )

    hx711.reset()   # Before we start, reset the HX711 (not obligate)
    measures = hx711.get_raw_data(num_measures=3)
finally:
    GPIO.cleanup()  # always do a GPIO cleanup in your scripts!

print("\n".join(measures))

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