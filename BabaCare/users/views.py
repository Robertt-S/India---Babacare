from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from users.forms import CadastroFormsBaba, CadastroFormsResponsavel
from users.models import Baba, Responsavel


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

def cadastro_baba(request):
    form = CadastroFormsBaba()

    if request.method == 'POST':
        form = CadastroFormsBaba(request.POST)

        if form.is_valid():

            nome1=form['nome_cadastro'].value()
            email1=form['email'].value()
            senha1=form['senha_1'].value()
            telefone1=form['telefone'].value()
            endereco1=form['endereco'].value()
            nascimento1=form['nascimento'].value()
            cpf1=form['cpf'].value()

            if form["senha_1"].value() != form["senha_2"].value():
                messages.error(request, 'Senhas não são iguais')
                return redirect('cadastro_baba')
            
            if Baba.objects.filter(cpf=cpf1).exists():
                messages.error(request, 'CPF já cadastrado.')
                return redirect('cadastro_baba')
            
            if Baba.objects.filter(email=email1).exists():
                messages.error(request, 'Email já cadastrado.')
                return redirect('cadastro_baba')
            
            if Baba.objects.filter(telefone=telefone1).exists():
                messages.error(request, 'Telefone já cadastrado.')
                return redirect('cadastro_baba')

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

    return render(request, 'users/register_baba.html', {'form': form})

def cadastro_responsavel(request):
    form = CadastroFormsResponsavel()

    if request.method == 'POST':
        form = CadastroFormsResponsavel(request.POST)

        if form.is_valid():

            nome1=form['nome_cadastro'].value()
            email1=form['email'].value()
            senha1=form['senha_1'].value()
            telefone1=form['telefone'].value()
            endereco1=form['endereco'].value()
            nascimento1=form['nascimento'].value()
            cpf1=form['cpf'].value()

            if form["senha_1"].value() != form["senha_2"].value():
                messages.error(request, 'Senhas não são iguais')
                return redirect('cadastro_responsavel')
            
            if Responsavel.objects.filter(cpf=cpf1).exists():
                messages.error(request, 'CPF já cadastrado.')
                return redirect('cadastro_responsavel')
            
            if Responsavel.objects.filter(email=email1).exists():
                messages.error(request, 'Email já cadastrado.')
                return redirect('cadastro_responsavel')
            
            if Responsavel.objects.filter(telefone=telefone1).exists():
                messages.error(request, 'Telefone já cadastrado.')
                return redirect('cadastro_responsavel')

            usuario = Responsavel.objects.create(
                nome=nome1,
                email=email1,
                senha=senha1,
                cpf=cpf1,
                telefone= telefone1,
                endereco=endereco1,
                nascimento=nascimento1
            )
            print('banana responsavel')
            usuario.save()
            messages.success(request, 'Cadastro efetuado com sucesso!')
            return redirect('login')

    return render(request, 'users/register_responsavel.html', {'form': form})