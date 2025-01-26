from django.forms import ModelForm
from django import forms
from users.models import Baba as Perfil_Baba
from users.models import Responsavel as Perfil_Responsavel

from django.views.generic.edit import UpdateView
from django.utils.timezone import now
from .models import Agenda, Servico

# "extends"

class EditBabaForm(ModelForm):
    
    bioBaba = forms.CharField(required=False, widget=forms.Textarea)
    habilidades = forms.CharField(required=False, widget=forms.Textarea)
    endereco = forms.CharField(required=True, label='CEP')
    numero = forms.CharField(required=True, label='Número da Residência')
    rangeTrabalho = forms.FloatField(required=True, label='Raio de Trabalho (km)')

    
    class Meta:
        model = Perfil_Baba
        fields = ('email','telefone','endereco','numero','bioBaba','habilidades','foto', 'rangeTrabalho')
        labels = {
            'email': 'Email',
            'telefone': 'Telefone',
            'endereco': 'CEP',
            'numero': 'Número da Residência',
            'bioBaba': 'Biografia',
            'habilidades': 'Habilidades',
            'foto': '',
            'rangeTrabalho': 'Raio de Trabalho (km)',
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


class AgendaRecorrenteForm(forms.Form):
    # Atualizando FREQUENCIAS para incluir todos os dias da semana
    FREQUENCIAS = [
        ('Segunda-feira', 'Segunda-feira'),
        ('Terça-feira', 'Terça-feira'),
        ('Quarta-feira', 'Quarta-feira'),
        ('Quinta-feira', 'Quinta-feira'),
        ('Sexta-feira', 'Sexta-feira'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]

    PERIODOS = [
        ('manhã', 'Manhã'),
        ('tarde', 'Tarde'),
        ('noite', 'Noite'),
    ]

    frequencia = forms.MultipleChoiceField(
        choices=FREQUENCIAS,
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    periodo = forms.MultipleChoiceField(
        choices=PERIODOS,
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    inicio_recorrencia = forms.DateField(widget=forms.SelectDateWidget())
    fim_recorrencia = forms.DateField(widget=forms.SelectDateWidget())

class ContratacaoForm(forms.Form):
    PERIODOS = [
        ('manhã', 'Manhã'),
        ('tarde', 'Tarde'),
        ('noite', 'Noite'),
    ]

    # baba = forms.ModelChoiceField(queryset=Perfil_Baba.objects.all(), required=True)  # Campo obrigatório para selecionar a babá
    data_servico = forms.DateField(widget=forms.SelectDateWidget(), required=True)  # Campo obrigatório para selecionar a data
    periodo = forms.ChoiceField(choices=PERIODOS, required=True)  # Campo obrigatório para selecionar o período