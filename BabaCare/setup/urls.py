"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.conf import settings
from django.views.static import serve
from users import views as v
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions, routers, serializers, viewsets

from users.models import BaseUser
from perfis.models import Perfil_Baba

app_name = 'main'

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['id','nome','cpf','nascimento','email','telefone','endereco','foto','criado','slug','isBaba','lat','long']

class UserViewSet(viewsets.ModelViewSet):
    queryset = BaseUser.objects.all()
    serializer_class = UserSerializer

User_doc = routers.DefaultRouter()
User_doc.register(r'Users', UserViewSet)

class PerfilSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Perfil_Baba
        fields = ['owner','nome_completo','data_nascimento','email','contato','endereco','cpf','link','slug','habilidades','foto']

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil_Baba.objects.all()
    serializer_class = PerfilSerializer

Perfil_doc = routers.DefaultRouter()
Perfil_doc.register(r'Perfis', PerfilViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title='BabaCare API',
        default_version='1.0.0'
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    path('', views.homepage,name="home"),
    path('about/',views.about),
    #path('users/',include('django.contrib.auth.urls')),
    path('users/',include('users.urls')),
    path('perfis/',include('perfis.urls'), name= 'perfis'),
    path('login/', v.login_view, name='login'),
    path('baba/cadastro/', v.cadastro_baba, name='cadastro_baba'),  #botao da linha azul
    path('responsavel/cadastro/', v.cadastro_responsavel, name='cadastro_responsavel'), #botao da linha azul
    
    path('api_doc/', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    path('perfis_doc/', include(User_doc.urls)),
    path('users_doc/', include(Perfil_doc.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
