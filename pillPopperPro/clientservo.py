# Referencing GPIO documentation at https://gpiozero.readthedocs.io/en/v1.5.1/recipes.html#servo
import socket

SERVER_ADDRESS = "2C:CF:67:7E:B0:E4"  
PORT = 1

client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
client.connect((SERVER_ADDRESS, PORT))

try:
    while True:
        angle = input("Enter angle (0-180): ")

        try:
            client.send(angle.encode('utf-8'))
            data = client.recv(1024)  
            print(f"Server response: {data.decode('utf-8')}")
        except ValueError:
            print("Please enter a valid integer.")

except OSError as e:
    pass

client.close()