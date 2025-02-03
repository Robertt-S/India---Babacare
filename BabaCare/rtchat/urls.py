from django.urls import path
from .views import *

app_name = 'rtchat'

urlpatterns = [
    path('', chatPage, name='chat-page'),
    path('<int:baba_id>/<int:resp_id>', privateChat, name='pv-chat'),
]
