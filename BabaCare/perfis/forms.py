from django.forms import ModelForm
from django import forms
from users.models import Baba as Perfil_Baba
from users.models import Responsavel as Perfil_Responsavel

from django.views.generic.edit import UpdateView

# "extends"

class EditBabaForm(ModelForm):
    
    bioBaba = forms.CharField(required=False, widget=forms.Textarea)
    habilidades = forms.CharField(required=False, widget=forms.Textarea)
    endereco = forms.CharField(required=True, label='CEP')
    numero = forms.CharField(required=True, label='Número da Residência')
    
    class Meta:
        model = Perfil_Baba
        fields = ('email','telefone','endereco','numero','bioBaba','habilidades','foto')
        labels = {
            'email': 'Email',
            'telefone': 'Telefone',
            'endereco': 'CEP',
            'numero': 'Número da Residência',
            'bioBaba': 'Biografia',
            'habilidades': 'Habilidades',
            'foto': '',
        }
        
class EditRespForm(ModelForm):
    
    bioResp = forms.CharField(required=False, widget=forms.Textarea)
    
    class Meta:
        model = Perfil_Responsavel
        fields = ('email','telefone','endereco', 'bioResp','foto')
        labels = {
            'email': 'Email',
            'contato': 'Telefone',
            'endereco': 'Endereço',
            'bioResp': 'Biografia',
            'foto': '',
        }