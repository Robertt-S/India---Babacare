from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.validators import validate_email
           
class CadastroFormsBaba(forms.Form):
    nome_cadastro=forms.CharField(
        label='Nome de Cadastro', 
        required=True, 
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: João Silva',
            }
        )
    )
    email=forms.EmailField(
        label='Email',
        required=True,
        max_length=100,
        validators=[validate_email],
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: joaosilva@xpto.com',
            }
        )
    )
    senha_1=forms.CharField(
        label='Senha', 
        required=True, 
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite a sua senha',
            }
        ),
    )
    senha_2=forms.CharField(
        label='Confirme a sua senha', 
        required=True, 
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite a sua senha novamente',
            }
        ),       
    )
    
    cpf = forms.CharField(
        label='CPF',
        required=True,
        max_length=11,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '1234567891',
            }
        ),
    )
    
    nascimento = forms.DateField(
        label='Data de Nascimento',
        required=True,
        
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'AAAA-MM-DD',
            }
        ),
    )
    
    endereco = forms.CharField(
        label='CEP',
        required=True,
        max_length=500,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '12345-678',
            }
        ),
    )
    
    numero = forms.CharField(
        label='Número da Residência',
        required=True,
        max_length=500,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite o número da residência',
            }
        ),
    )
    
    telefone = forms.CharField(
        label='Telefone',
        required=True,
        max_length=20,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '11233334444',
            }
        ),
    )


class CadastroFormsResponsavel(forms.Form):
    nome_cadastro=forms.CharField(
        label='Nome de Cadastro', 
        required=True, 
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: João Silva',
            }
        )
    )
    email=forms.EmailField(
        label='Email',
        required=True,
        max_length=100,
        validators=[validate_email],
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: joaosilva@xpto.com',
            }
        )
    )
    senha_1=forms.CharField(
        label='Senha', 
        required=True, 
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite a sua senha',
            }
        ),
    )
    senha_2=forms.CharField(
        label='Confirme a sua senha', 
        required=True, 
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite a sua senha novamente',
            }
        ),       
    )
    
    cpf = forms.CharField(
        label='CPF',
        required=True,
        max_length=11,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '1234567891',
            }
        ),
    )
    
    nascimento = forms.DateField(
        label='Data de Nascimento',
        required=True,
        
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'AAAA-MM-DD',
            }
        ),
    )
    
    endereco = forms.CharField(
        label='CEP',
        required=True,
        max_length=11,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '12345-678',
            }
        ),
    )
    
    numero = forms.CharField(
        label='Número da Residência',
        required=True,
        max_length=10,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite o número da residência',
            }
        ),
    ) 
    
    telefone = forms.CharField(
        label='Telefone',
        required=True,
        max_length=20,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '11233334444',
            }
        ),
    )