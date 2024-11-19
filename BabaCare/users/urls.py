from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'users'

urlpatterns = [
    path('register/', views.register_user, name="register"),
    path('login/',views.login_view, name="login"),
    path('logout/', views.logout_view,name="logout"),
    path('baba/', views.baba_page, name='baba_page'),
    path('responsaveis/', views.responsaveis_page, name='responsaveis_page')
    ]



if settings.DEBUG:
    urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)