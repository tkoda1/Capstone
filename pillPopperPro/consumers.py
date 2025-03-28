from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
# from .client import *




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

        self.broadcast_data({'action': 'connection'})
        # connect_to_server()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )
        #disconnect_from_server()

    def receive(self, **kwargs):
        print("RECEIVING DATA")
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

        if action == 'release':
            # send_message_to_server()
            self.broadcast_data(data)
            return

        self.send_error(f'Invalid action property: "{action}"')

        self.broadcast_data(data)

    
    def send_error(self, error_message):
        self.send(text_data=json.dumps({'error': error_message}))


    def broadcast_data(self, data):
        print("BROADCASTING DATA")
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'broadcast_event',
                'message': json.dumps(data)
            }
        )
    
    def broadcast_event(self, event):
        self.send(text_data=event['message'])

  