from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'users'

urlpatterns = [
    path('cadastro_baba/', views.cadastro_baba, name="registro_baba"),  # URL única
    path('cadastro_responsavel/', views.cadastro_responsavel, name="registro_responsavel"),  # URL única
    path('logout/', views.logout_view, name="logout"),
    path('baba/', views.baba_page, name='baba_page'),
    path('responsaveis/', views.responsaveis_page, name='responsaveis_page'),
    path('home_baba/', views.home_baba, name="home_baba"),
    path('home_responsavel/', views.home_responsavel, name="home_responsavel"),
]

if settings.DEBUG:
    urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)