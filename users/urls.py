from django.urls import path
from . import views

#esses urls estão dentro do app users
app_name = 'users'

# when a request to these specific pages are made, views will process the request
urlpatterns = [
  path('baba/',views.CadastroDaBaba,name='CadastroDaBaba'),
  path('responsavel/',views.CadastroDoResponsavel,name='CadastroDoResponsavel'),
  path('cadresponsavel/',views.aposCadastroResp,name='cadResponsaveis'),
  path('cadbaba/', views.aposCadastroBabas, name='cadBabas'),
  path('lista_resposavel/', views.Responsaveis, name='listaResponsaveis'),
  path('lista_baba/', views.Babas, name='listaBabas'),
]