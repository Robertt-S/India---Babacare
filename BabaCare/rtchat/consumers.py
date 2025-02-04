# This .py is where all the async functionalities will take place
# ASYNC

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime
from rtchat.models import Mensagem
from users.models import Baba, Responsavel
from channels.db import database_sync_to_async

# Para criar e destruir algumas coisas em WebSockets
class ChatConsumer(AsyncWebsocketConsumer):
    # Cria o nome de grupo para o chat e adiciona o group para os channel layers
    async def connect(self):
        self.baba_id = self.scope['url_route']['kwargs']['baba_id']
        self.resp_id = self.scope['url_route']['kwargs']['resp_id']
        self.roomGroupName = f"chat_{self.baba_id}_{self.resp_id}"
        
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
    #JSON -> Dicionario
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        user_avatar = text_data_json["user_avatar"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        nova_mensagem = await self.salvar_mensagem(message, self.scope['user'], self.baba_id, self.resp_id)
        
        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": nova_mensagem.conteudo,
                "username": username,
                "user_avatar": user_avatar,
                "timestamp": timestamp
            }
        )
        
    # Envia a mensagem e o username para todos no grupo como um JSON (dicionario)
    async def sendMessage(self , event) : 
        message = event["message"]
        username = event["username"]
        user_avatar = event["user_avatar"]
        timestamp = event["timestamp"]
        
        await self.send(text_data = json.dumps({
            "message":message ,
            "username":username, 
            "user_avatar":user_avatar,
            "timestamp":timestamp
        }))
        
    @database_sync_to_async
    def salvar_mensagem(self, mensagem, usuario, baba_id, resp_id):
        baba = Baba.objects.get(id=baba_id)
        responsavel = Responsavel.objects.get(id=resp_id)
        autor = usuario
        nova_mensagem = Mensagem(
            baba=baba,
            responsavel=responsavel,
            autor=autor,
            conteudo=mensagem,
        )
        nova_mensagem.save()
        return nova_mensagem