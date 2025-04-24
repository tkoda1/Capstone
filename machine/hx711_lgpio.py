# https://chatgpt.com/share/67f85111-754c-8000-b1ac-096d6783ee33

import lgpio
import time

class HX711:
    def __init__(self, dout_pin, pd_sck_pin, gain=128):
        self.dout_pin = dout_pin
        self.pd_sck_pin = pd_sck_pin
        self.gain = gain

        self.lgpio_handle = lgpio.gpiochip_open(0)
        lgpio.gpio_claim_input(self.lgpio_handle, self.dout_pin)
        lgpio.gpio_claim_output(self.lgpio_handle, self.pd_sck_pin)

        self.offset = 0
        self.scale = 1
        self.set_gain()

    def set_gain(self):
        if self.gain == 128:
            self.GAIN = 1
        elif self.gain == 64:
            self.GAIN = 3
        elif self.gain == 32:
            self.GAIN = 2

        # wake up HX711
        lgpio.gpio_write(self.lgpio_handle, self.pd_sck_pin, 0)
        self.read_raw()

    def is_ready(self):
        return lgpio.gpio_read(self.lgpio_handle, self.dout_pin) == 0

    def read_raw(self):
        while not self.is_ready():
            time.sleep(0.001)

        data = 0
        for _ in range(24):
            lgpio.gpio_write(self.lgpio_handle, self.pd_sck_pin, 1)
            data = data << 1
            lgpio.gpio_write(self.lgpio_handle, self.pd_sck_pin, 0)
            if lgpio.gpio_read(self.lgpio_handle, self.dout_pin):
                data += 1

        for _ in range(self.GAIN):
            lgpio.gpio_write(self.lgpio_handle, self.pd_sck_pin, 1)
            lgpio.gpio_write(self.lgpio_handle, self.pd_sck_pin, 0)

        if data & 0x800000:
            data |= ~0xffffff

        return data

    def read_average(self, times=3):
        values = [self.read_raw() for _ in range(times)]
        return sum(values) / len(values)

    def get_raw_data_mean(self, times=3):
        return self.read_average(times)

    def get_weight_mean(self, times=3):
        value = self.read_average(times)
        return (value - self.offset) / self.scale

    def tare(self, times=15):
        self.offset = self.read_average(times)

    def set_scale(self, scale):
        self.scale = scale

    def reset(self):
        self.set_gain()

    def zero(self):
        self.tare()

    def power_down(self):
        lgpio.gpio_write(self.lgpio_handle, self.pd_sck_pin, 0)
        lgpio.gpio_write(self.lgpio_handle, self.pd_sck_pin, 1)

    def cleanup(self):
        lgpio.gpiochip_close(self.lgpio_handle)
