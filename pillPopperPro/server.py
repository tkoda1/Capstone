# source to see if bluetooth is working: https://www.youtube.com/watch?v=8pMaR-WUc6U

import socket

SERVER_ADDRESS = "2C:CF:67:7E:B0:E4"  # Replace with Raspberry Pi's Bluetooth MAC
PORT = 1

server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
server.bind((SERVER_ADDRESS, PORT))
server.listen(PORT)

client, addr = server.accept()

try:
    while True:
        data = client.recv(1024)
        if not data:
            break
        print(f"Message: {data.decode('utf-8')}")
        message = input("Enter Message: ")
        client.send(message.encode("utf-8"))
except OSError as e:
    pass

client.close()
server.close()