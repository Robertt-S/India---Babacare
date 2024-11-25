from django.forms import ModelForm
from django import forms
from users.models import Baba as Perfil_Baba

from django.views.generic.edit import UpdateView

# "extends"

class EditProfileForm(ModelForm):
    class Meta:
        model = Perfil_Baba
        fields = ('email','telefone','endereco','foto')
        labels = {
            'email': 'Email',
            'contato': 'Telefone',
            'endereco': 'Endereço',
            'foto': '',
        }
        
        