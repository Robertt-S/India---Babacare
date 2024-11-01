from django.urls import path
from . import views

#esses urls estão dentro do app users
app_name = 'users'

# when a request to these specific pages are made, views will process the request
urlpatterns = [
  path('baba/',views.CadastroDaBaba,name='CadastroDaBaba'),
  path('responsavel/',views.CadastroDoResponsavel,name='CadastroDoResponsavel'),
  path('lista_responsavel/',views.Responsaveis,name='Responsaveis'),
  path('lista_baba/', views.Babas, name='Babas')
]