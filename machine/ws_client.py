# https://pypi.org/project/websocket-client/
# https://websockets.readthedocs.io/en/stable/intro/tutorial1.html
# pip install websocket-client

import websocket
from constants import WEBSOCKET_URL, LOAD_CELL_ERROR
import _thread
import time
import rel
import json
import servo, speaker
# import loadcell

def on_message(ws, message):
    print(f"Received message: {message}")
    data = json.loads(message)
    if not data or not data["action"]:
        on_error(ws, "Invalid data sent")
    elif data["action"] == "release":
        release_pill(data)
    elif data["action"] == "refill":
        refill_reminder(data)
    else:
        on_error(ws, f"Invalid action: {data['action']}")

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

def release_pill(data):
    print("Releasing pill")
    if not data["slot"]:
        on_error(ws, "Invalid pill slot sent")
    # initial_weight = loadcell.read_weight()
    speaker.play_release_pill()
    servo.dispense_pill(int(data["slot"])-1)
    # final_weight = loadcell.read_weight()
    # if (final_weight - initial_weight < LOAD_CELL_ERROR):
    #     on_error(f"Pill not dispensed initial: {initial_weight} final: {final_weight}")
    #     speaker.play_not_dispensed()
    #     return
    speaker.play_finish_dispensing()

def refill_reminder(data):
    print("Refill reminder")
    if not data["slot"]:
        on_error(ws, "Invalid pill slot sent for reminder")
    speaker.play_refill_reminder()

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