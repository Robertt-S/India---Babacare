# This .py will route the WebSocket connections to the consumers
# ASYNC

from django.urls import path , include
from rtchat.consumers import ChatConsumer

# Here, "" is routing to the URL ChatConsumer which 
# will handle the chat functionality.
# os urls daqui NÃO TEM NADA HAVER com os do urls.py
websocket_urlpatterns = [
    path("" , ChatConsumer.as_asgi()),
    path('ws/chat/<int:user1_id>/<int:user2_id>/', ChatConsumer.as_asgi()),
] 