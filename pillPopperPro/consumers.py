from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

# CODE THAT USES MQTT - try to see if this works with the RPI
# import paho.mqtt.client as mqtt


class PillPopperProConsumer(WebsocketConsumer):
    group_name = 'pillPopperPro_group'
    channel_name = 'pillPopperPro_channel'

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )

        self.accept()

        # if not self.scope["user"].is_authenticated:
        #     self.send_error(f'You must be logged in')
        #     self.close()
        #     return

        # if not self.scope["user"].email.endswith("@andrew.cmu.edu"):
        #     self.send_error(f'You must be logged with Andrew identity')
        #     self.close()
        #     return            

        # self.user = self.scope["user"]

        self.broadcast_data()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )

    def receive(self, **kwargs):
        # can add storage information here
        if 'text_data' not in kwargs:
            self.send_error('you must send text_data')
            return

        try:
            data = json.loads(kwargs['text_data'])
        except json.JSONDecoder:
            self.send_error('invalid JSON sent to server')
            return

        if 'action' not in data:
            self.send_error('action property not sent in JSON')
            return

        action = data['action']

        if action == 'add':
            self.broadcast_data()
            return

        self.send_error(f'Invalid action property: "{action}"')

        self.broadcast_data()

        # CODE THAT USES MQTT
        # if data.get("command") == "DISPENSE": # edit based on the actuals dispense comand
            # client = mqtt.Client()
            # client.connect("OUR_MQTT_BROKER_IP", 1883)
            # client.publish("pill_dispenser/command", "DISPENSE")
            # client.disconnect()

            # await self.send(text_data=json.dumps({"message": "Dispensing initiated"}))

    def send_error(self, error_message):
        self.send(text_data=json.dumps({'error': error_message}))


    def broadcast_data(self):
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'broadcast_event',
                'message': json.dumps({'hello': 'world'})
            }
        )
    
    def broadcast_event(self, event):
        self.send(text_data=event['message'])

    # CODE THAT USES MQTT
    # def send_dispense_status(self):
    #     client = mqtt.Client()
        
    #     def on_message(client, userdata, message):
    #         status = message.payload.decode()
    #         if status == "DISPENSED":
    #             self.send(text_data=json.dumps({"message": "Pill dispensed"}))
        
    #     client.on_message = on_message
    #     client.connect("YOUR_MQTT_BROKER_IP", 1883)
    #     client.subscribe("pill_dispenser/status")
    #     client.loop_start()
