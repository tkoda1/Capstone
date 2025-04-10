# https://chatgpt.com/share/67f838f5-88b0-8000-88a2-48a3be3861d8

import time
from hx711 import HX711

DT_PIN = 5
SCK_PIN = 6

hx = HX711(DT_PIN, SCK_PIN)
hx.reset()
hx.zero()

print("Reading raw-ish value (averaged):")
print(hx.get_raw_data_mean())

print("Now reading weight:")
try:
    while True:
        weight = hx.get_weight_mean(5)
        print(f"Weight: {weight:.2f} units")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Exiting...")
    hx.power_down()
    hx.cleanup()
