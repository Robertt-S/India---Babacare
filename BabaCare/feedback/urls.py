from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('<contract>', views.feedback_page, name="feedback_page"),
    path('feedback_edit_page/<contract>/', views.edit_feedback, name="give_feedback")
]