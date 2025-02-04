# This .py will route the WebSocket connections to the consumers
# ASYNC

from django.urls import path , include, re_path
from rtchat.consumers import ChatConsumer

# Here, "" is routing to the URL ChatConsumer which 
# will handle the chat functionality.
# os urls daqui NÃO TEM NADA HAVER com os do urls.py
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<baba_id>\d+)/(?P<resp_id>\d+)/$', ChatConsumer.as_asgi()),
]