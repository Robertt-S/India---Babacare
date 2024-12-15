from django.urls import path
from . import views

app_name = 'perfis'

urlpatterns = [
    path('', views.baba_list, name="lista_babas"),
    path('edit_page/<perfil_id>/', views.edit_page,name="edit_page"),
    path('my_page/',views.my_page,name="my_page"),
    path('<slug:slug>', views.page_baba, name="page_baba"),
]