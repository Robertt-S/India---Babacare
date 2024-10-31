from django.urls import path
from . import views

#esses urls estão dentro do app posts
app_name = 'posts'

# when a request to these specific pages are made, views will process the request
urlpatterns = [
    path('', views.posts_list, name="list"),
    path('<slug:slug>', views.post_page, name="page"),
]