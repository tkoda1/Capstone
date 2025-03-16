import socket

SERVER_ADDRESS = "2C:CF:67:7E:B0:E4"  # Replace with Raspberry Pi's Bluetooth MAC
PORT = 1

# Set up the Bluetooth client
client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
client.connect((SERVER_ADDRESS, PORT))

try:
    while True:
        # Get the angle from the user
        angle = input("Enter angle (0-180): ")

        try:
            # Send the angle to the server
            client.send(angle.encode('utf-8'))
            data = client.recv(1024)  # Wait for the server's response
            print(f"Server response: {data.decode('utf-8')}")
        except ValueError:
            print("Please enter a valid integer.")

except OSError as e:
    pass

client.close()