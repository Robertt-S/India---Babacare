from django.urls import path
from . import views

# when a request to these specific pages are made, views will process the request
urlpatterns = [
    path('', views.posts_list),
]