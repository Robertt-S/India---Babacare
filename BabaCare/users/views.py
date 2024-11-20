from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from users.forms import CadastroForms
from users.models import Baba

# Create your views here.
# def register_user(request):
#     if request.method == "POST":
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             messages.success(request, ("Registration sucessful"))
#             return redirect('home')
            
#     else:
#         form = RegisterUserForm()
        
#     return render(request,'users/register.html', {'form':form})


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ("Houve um erro ao logar!"))
            return redirect('users:login')
    else:
        return render(request, 'users/login.html')
    

def logout_view(request):
    logout(request)
    messages.success(request, ("You're logged out!"))
    return redirect('home')

def baba_page(request):
    return render(request, 'baba.html')

def responsaveis_page(request):
    return render(request, 'responsaveis.html')

def cadastro(request):
    form = CadastroForms()

    if request.method == 'POST':
        form = CadastroForms(request.POST)

        if form.is_valid():
            if form["senha_1"].value() != form["senha_2"].value():
                messages.error(request, 'Senhas não são iguais')
                return redirect('cadastro')

            nome1=form['nome_cadastro'].value()
            email1=form['email'].value()
            senha1=form['senha_1'].value()
            telefone1=form['telefone'].value()
            endereco1=form['endereco'].value()
            nascimento1=form['nascimento'].value()
            cpf1=form['cpf'].value()

            if Baba.objects.filter(nome=nome1).exists():
                messages.error(request, 'Usuário já existente')
                return redirect('cadastro')

            usuario = Baba.objects.create(
                nome=nome1,
                email=email1,
                senha=senha1,
                cpf=cpf1,
                telefone= telefone1,
                endereco=endereco1,
                nascimento=nascimento1
            )
            print('banana')
            usuario.save()
            messages.success(request, 'Cadastro efetuado com sucesso!')
            return redirect('login')

    return render(request, 'users/register.html', {'form': form})