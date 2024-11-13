from django.forms import ModelForm
from django import forms
from .models import Perfil_Baba

from django.views.generic.edit import UpdateView

# "extends"

class EditProfileForm(ModelForm):
    class Meta:
        model = Perfil_Baba
        fields = ('email','contato','endereco','habilidades','foto')
        labels = {
            'email': 'Email',
            'contato': 'Telefone',
            'endereco': 'Endereço',
            'habilidades': 'Habilidades',
            'foto': '',
        }
        
        