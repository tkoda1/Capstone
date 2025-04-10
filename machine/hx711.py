# hx711.py
# https://chatgpt.com/share/67f84ea9-6f64-8000-91a1-147f733ab669

import time
import lgpio

class HX711:
    def __init__(self, dout, pd_sck, gain=128):
        self.dout = dout
        self.pd_sck = pd_sck
        self.gain = gain
        self.offset = 0
        self.scale = 1

        self.h = lgpio.gpiochip_open(0)  # Open the default GPIO chip
        lgpio.gpio_claim_input(self.h, self.dout)
        lgpio.gpio_claim_output(self.h, self.pd_sck)

        self.set_gain()

    def is_ready(self):
        return lgpio.gpio_read(self.h, self.dout) == 0

    def set_gain(self):
        if self.gain == 128:
            self.GAIN = 1
        elif self.gain == 64:
            self.GAIN = 3
        elif self.gain == 32:
            self.GAIN = 2
        lgpio.gpio_write(self.h, self.pd_sck, 0)
        self.read_raw()

    def read_raw(self):
        while not self.is_ready():
            time.sleep(0.001)

        count = 0
        for _ in range(24):
            lgpio.gpio_write(self.h, self.pd_sck, 1)
            count = count << 1 | lgpio.gpio_read(self.h, self.dout)
            lgpio.gpio_write(self.h, self.pd_sck, 0)

        # Set gain
        for _ in range(self.GAIN):
            lgpio.gpio_write(self.h, self.pd_sck, 1)
            lgpio.gpio_write(self.h, self.pd_sck, 0)

        # Convert from 2's complement
        if count & 0x800000:
            count |= ~0xffffff

        return count

    def read_average(self, times=3):
        sum_val = 0
        for _ in range(times):
            sum_val += self.read_raw()
        return sum_val / times

    def tare(self, times=15):
        self.offset = self.read_average(times)

    def get_weight(self, times=3):
        value = self.read_average(times)
        return (value - self.offset) / self.scale

    def set_scale(self, scale):
        self.scale = scale

    def cleanup(self):
        lgpio.gpiochip_close(self.h)
