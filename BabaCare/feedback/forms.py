from django import forms
from django.forms import ModelForm
from .models import Feedback

class FeedbackForms (ModelForm):
    
    score = forms.IntegerField(required=True, min_value=0, max_value=10, widget=forms.TextInput, label="Nota")

    class Meta:
        model = Feedback
        fields = ["title", "score", "description"]
        labels={
            "title": "Título da Avaliação",
            "score": "Nota (0 - 5)",
            "description": "Avaliação"
        }