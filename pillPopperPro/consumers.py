# from channels.generic.websocket import WebsocketConsumer
# from asgiref.sync import async_to_sync
# import json

# class PillPopperProConsumer(WebsocketConsumer):
#     group_name = 'pillPopperPro_group'
#     channel_name = 'pillPopperPro_channel'

#     def connect(self):
#         async_to_sync(self.channel_layer.group_add)(
#             self.group_name, self.channel_name
#         )

#         self.accept()

#         if not self.scope["user"].is_authenticated:
#             self.send_error(f'You must be logged in')
#             self.close()
#             return

#         if not self.scope["user"].email.endswith("@andrew.cmu.edu"):
#             self.send_error(f'You must be logged with Andrew identity')
#             self.close()
#             return            

#         self.user = self.scope["user"]

#         self.broadcast_list()

#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.group_name, self.channel_name
#         )