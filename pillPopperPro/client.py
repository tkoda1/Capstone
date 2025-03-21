# source to see if bluetooth is working: https://www.youtube.com/watch?v=8pMaR-WUc6U
'''
import socket, threading


SERVER_ADDRESS = "2C:CF:67:7E:B0:E4"  
PORT = 1
client, thread = None, None

def connect_to_server():
    client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    client.connect((SERVER_ADDRESS, PORT))
    thread = threading.Tread(target=receive_message_from_server)
    thread.start()

def send_message_to_server():
    message = input('Released. Enter message: ')
    client.send(message.encode('utf-8'))

def receive_message_from_server():
    data = client.recv(1024)
    if not data:
        return
    print(f"Message: {data.decode('utf-8')}")

def disconnect_from_server():
    thread.join()
    client.close()

'''
# source to see if bluetooth is working: https://www.youtube.com/watch?v=8pMaR-WUc6U

import socket


SERVER_ADDRESS = "2C:CF:67:7E:B0:E4"  
PORT = 1

client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
client.connect((SERVER_ADDRESS, PORT))


try:
    while True:
        message = input('Enter message: ')
        client.send(message.encode('utf-8'))
        data = client.recv(1024)
        if not data:
            break
        print(f"Message: {data.decode('utf-8')}")
except OSError as e:
    pass

client.close()