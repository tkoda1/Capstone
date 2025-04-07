# https://chatgpt.com/share/67f4049b-cb10-8000-851c-a615b98f2cc0

import time
from hx711 import HX711  # Use hx711py or the hx711.py file from the repo

# GPIO pin setup (BCM numbering)
DT_PIN = 5    # Replace with your actual pin
SCK_PIN = 6   # Replace with your actual pin

hx = HX711(DT_PIN, SCK_PIN)

# Set scale ratio based on calibration (default for testing)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(1)  # Set later after calibration

hx.reset()
hx.tare()

print("Tare done. Place an object on the load cell...")

try:
    while True:
        weight = hx.get_weight(5)  # Average of 5 readings
        print(f"Weight: {weight:.2f} units")
        time.sleep(0.5)
        hx.power_down()
        hx.power_up()
except KeyboardInterrupt:
    print("Exiting...")