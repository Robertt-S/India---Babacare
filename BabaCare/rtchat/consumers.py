# This .py is where all the async functionalities will take place
# ASYNC

import json
from channels.generic.websocket import AsyncWebsocketConsumer

# Para criar e destruir algumas coisas em WebSockets
class ChatConsumer(AsyncWebsocketConsumer):
    # Cria o nome de grupo para o chat e adiciona o group para os channel layers
    async def connect(self):
        self.roomGroupName = "group_chat_gfg"
        await self.channel_layer.group_add(
            self.roomGroupName ,
            self.channel_name
        )
        await self.accept()
    # Remove a instancia do group
    async def disconnect(self , close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName , 
            self.channel_name 
        )
        
    # Ativada quando mandamos dados para o WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        await self.channel_layer.group_send(
            self.roomGroupName,{
                "type" : "sendMessage" ,
                "message" : message , 
                "username" : username
            })
    # Envia a mensagem e o username para todos no grupo como um JSON (dicionario)
    async def sendMessage(self , event) : 
        message = event["message"]
        username = event["username"]
        await self.send(text_data = json.dumps({"message":message ,"username":username}))