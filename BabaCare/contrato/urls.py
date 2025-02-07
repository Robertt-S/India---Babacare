from django.urls import path
from . import views

app_name = 'contrato'

urlpatterns = [
    path('', views.baba_list, name="lista_babas"),
    path('contratar_servico/<id>/', views.contratar_servico, name='contratar_servico'),
    path('gerenciar_servicos/', views.gerenciar_servicos, name='gerenciar_servicos'),
    path('servicos_responsavel/', views.servicos_responsavel, name='servicos_responsavel'),
]