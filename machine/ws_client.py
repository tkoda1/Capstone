# https://pypi.org/project/websocket-client/
# https://websockets.readthedocs.io/en/stable/intro/tutorial1.html
# pip install websocket-client

import websocket
from constants import WEBSOCKET_URL
import _thread
import time
import rel
import json
# import loadcell
import servo

def on_message(ws, message):
    print(f"Received message: {message}")
    data = json.loads(message)
    if not data or not data["action"]:
        on_error(ws, "Invalid data sent")
    elif data["action"] == "release":
        print("Releasing pill")
        if not data["slot"]:
            on_error(ws, "Invalid pill slot sent")
        servo.dispense_pill(int(data["slot"])-1)
    else:
        on_error(ws, f"Invalid action: {data['action']}")

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

def send_message(ws, message):
    ws.send(json.dumps(message))

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(WEBSOCKET_URL,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()