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
        
        
        
        
        
        
class CadastroForms(forms.Form):
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
                'placeholder': '12/07/2001',
            }
        ),
    )
    
    endereco = forms.CharField(
        label='Endereço',
        required=True,
        max_length=500,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Rua Patati e Patata, 500',
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