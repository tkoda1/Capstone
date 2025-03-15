import pigpio

pi = pigpio.pi()

if not pi.connected:
    print("Failed to connect to pigpio daemon!")
else:
    print("pigpio is running!")
    pi.stop()