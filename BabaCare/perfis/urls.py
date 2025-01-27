from django.urls import path
from . import views

app_name = 'perfis'

urlpatterns = [
    path('', views.baba_list, name="lista_babas"),
    path('edit_page/<perfil_id>/', views.edit_page,name="edit_page"),
    path('my_page/',views.my_page,name="my_page"),
    path('<slug:slug>', views.page_baba, name="page_baba"),
    path('agenda_recorrente/', views.agenda_recorrente, name='agenda_recorrente'),
    path('buscar/', views.buscar, name='buscar' ),
    path('contratar_servico/<id>/', views.contratar_servico, name='contratar_servico'),
    path('gerenciar_servicos/', views.gerenciar_servicos, name='gerenciar_servicos'),
    #path('servicos_finalizados/', views.servicos_finalizados, name='servicos_finalizados'),
]