import socket

SERVER_ADDRESS = "2C:CF:67:7E:B0:E4"  
PORT = 1

client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
client.connect((SERVER_ADDRESS, PORT))

try:
    while True:
        slot = input("Enter slot (0-5) or 'q' to quit: ")
        if slot.lower() == 'q':
            break

        angle = input("Enter angle (0-180): ")

        try:
            slot = int(slot)
            angle = int(angle)

            if 0 <= slot <= 5 and 0 <= angle <= 180:
                message = f"{slot},{angle}"  # Sending both slot and angle
                client.send(message.encode('utf-8'))
                data = client.recv(1024)
                print(f"Server response: {data.decode('utf-8')}")
            else:
                print("Slot must be 0-5 and angle must be 0-180.")

        except ValueError:
            print("Please enter valid numbers for slot and angle.")

except OSError as e:
    print(f"Error: {e}")

finally:
    client.close()
