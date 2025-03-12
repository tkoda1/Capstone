import bluetooth
import time
from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO
from hx711 import HX711

# Initialize Servo Driver (PCA9685)
kit = ServoKit(channels=16)

# Define the servo motor channel
SERVO_CHANNEL = 0  # Adjust based on your setup
SERVO_OPEN_ANGLE = 180  # Adjust angle for dispensing
SERVO_CLOSE_ANGLE = 0  # Default position

# Initialize Load Cell (Weight Sensor)
hx = HX711(dout=5, pd_sck=6)  # GPIO pins for data and clock
hx.set_reference_unit(1)  # Calibrate this value based on your load cell
hx.reset()
hx.tare()  # Tare weight sensor

# Bluetooth Configuration
SERVER_ADDRESS = "B8:27:EB:00:00:00"  # Replace with Raspberry Pi's Bluetooth MAC
PORT = 1

def setup_bluetooth():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind((SERVER_ADDRESS, PORT))
    server_sock.listen(1)
    print("Waiting for Bluetooth connection...")
    
    client_sock, address = server_sock.accept()
    print(f"Connected to {address}")
    return client_sock

def dispense_pill():
    """Rotates servo motor to dispense a pill"""
    print("Dispensing pill...")
    kit.servo[SERVO_CHANNEL].angle = SERVO_OPEN_ANGLE  # Open slot
    time.sleep(1)  # Allow time for pill to drop
    kit.servo[SERVO_CHANNEL].angle = SERVO_CLOSE_ANGLE  # Close slot

    # Verify pill has been dispensed using weight sensor
    time.sleep(2)  # Allow pill to settle on load cell
    weight = hx.get_weight(5)
    if weight > 500:  # Adjust threshold based on pill weight
        print("Pill successfully dispensed!")
    else:
        print("Error: No pill detected!")

def main():
    client_sock = setup_bluetooth()
    
    try:
        while True:
            data = client_sock.recv(1024).decode('utf-8').strip()
            if data == "DISPENSE":
                dispense_pill()
                client_sock.send("PILL_DISPENSED")
            elif data == "EXIT":
                break
    except KeyboardInterrupt:
        print("Shutting down...")
    
    client_sock.close()

if __name__ == "__main__":
    main()
