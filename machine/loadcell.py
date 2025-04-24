# https://chatgpt.com/share/67f838f5-88b0-8000-88a2-48a3be3861d8

import time
from hx711 import HX711

# Set GPIO pins (BCM numbering)
DT_PIN = 5    # Data pin from HX711
SCK_PIN = 6   # Clock pin to HX711

# Create HX711 object
hx = HX711(dout=DT_PIN, pd_sck=SCK_PIN)

# Optional: adjust this depending on your load cell and wiring
hx.set_reading_format("MSB", "MSB")

# Reset and zero the scale
hx.reset()
hx.tare()

print("Taring complete. Place weight on the scale.")

readings = []

try:
    while True:
        weight = hx.get_weight(5)  # average over 5 readings
        readings.append(weight)

        if len(readings) > 10:
            readings.pop(0)

        avg_weight = sum(readings) / len(readings)
        print(f"Smoothed Weight: {avg_weight:.2f} units")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    hx.power_down()
    hx.power_up()
