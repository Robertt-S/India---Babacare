from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# "extends"

class RegisterUserForm(UserCreationForm):
    # o que eu quero adicionar na hora de se registrar
    email = forms.EmailField()
    nome_completo= forms.CharField(max_length=255)
    cpf = forms.CharField(max_length=11)
    
    class Meta:
        model = User
        fields = ('nome_completo', 'email', 'cpf', 'username', 'password1', 'password2')