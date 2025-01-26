from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('<int:contract.id>', views.feedback_page, name="feedback_page"),
    path('feedback_edit_page/<int:contract.id>/', views.edit_feedback, name="give_feedback")
]