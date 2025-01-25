from django import forms

class FeedbackForms (forms.Form):
    forms_title=forms.CharField(
        label="Título da Avaliação",
        required=True,
        max_length=100,
        widget=forms.CharField(
            attrs={
                'class': 'form-control',
                'placeholder': 'Título da avaliação'
            }
        )
    )
    forms_score=forms.IntegerField(
        label="Nota da Avaliação",
        required=True,
        min_value=0,
        max_value=10,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nota'
            }
        )
    )
    forms_description=forms.CharField(
        label="Descrição da Avaliação",
        required=True,
        max_length=500,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Sua avaliação'
            }
        )
    )