from django.forms import ModelForm
from django import forms
from .models import Perfil_Baba

# "extends"

class EditProfileForm(ModelForm):
    class Meta:
        model = Perfil_Baba
        fields = ('email','contato','endereco','habilidades','foto')