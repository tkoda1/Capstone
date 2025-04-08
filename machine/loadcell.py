# https://chatgpt.com/share/67f5a57f-6140-8000-944d-e7f2a07be261

import time
from hx711 import HX711

DT_PIN = 5
SCK_PIN = 6

hx = HX711(DT_PIN, SCK_PIN)

hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(1)  # Placeholder — update after calibration

hx.reset()
# hx.tare()  # Comment this out to see raw values

print("Reading raw-ish value (averaged):")
print(hx.read_average(times=10))

print("Now reading weight:")
try:
    while True:
        weight = hx.get_weight(5)
        print(f"Weight: {weight:.2f} units")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Exiting...")
