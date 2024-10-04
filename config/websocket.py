# async def websocket_application(scope, receive, send):
#     while True:
#         event = await receive()

#         if event["type"] == "websocket.connect":
#             await send({"type": "websocket.accept"})

#         if event["type"] == "websocket.disconnect":
#             break

#         if event["type"] == "websocket.receive":
#             if event["text"] == "ping":
#                 await send({"type": "websocket.send", "text": "pong!"})


from channels.generic.websocket import JsonWebsocketConsumer

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync


class IpScanner(AsyncWebsocketConsumer):

    async def connect(self):
        print('Connected on Web Socket!')
        self.user = self.scope['user']
        if self.user.is_authenticated:

            self.group_name = f'user_{self.user.username}'
            
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )

            await self.accept()
        else:
            print("User is not authenticated.")
            await self.close()
    async def disconnect(self, close_code):
        # Leave the group on disconnect
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_ip_info(self, event):
        # Send IP info back to the user
        await self.send(text_data=json.dumps(event['ip_info']))
