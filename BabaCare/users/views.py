from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from users.forms import CadastroFormsBaba, CadastroFormsResponsavel
from users.models import Baba, Responsavel
from django.utils import timezone
from datetime import datetime
from validate_docbr import CPF
import dns.resolver



def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
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
    cpf = CPF()

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
            
            
            if not verificar_registros_mx(email1):
                messages.error(request, 'O domínio do e-mail não é válido ou não aceita mensagens.')
                return redirect('cadastro_baba')
            
            #idade
            nascimento_str = request.POST.get('nascimento')  
            try:
                nascimento1 = datetime.strptime(nascimento_str, '%Y-%m-%d').date() 
            except (ValueError, TypeError):
                messages.error(request, 'Data de nascimento inválida. Use o formato AAAA-MM-DD.')
                return redirect('cadastro_baba')

            # Calcula a idade
            hoje = timezone.now().date()
            idade = hoje.year - nascimento1.year - ((hoje.month, hoje.day) < (nascimento1.month, nascimento1.day))

            if idade < 18:
                messages.error(request, 'Faixa etária não permitida.')
                return redirect('cadastro_baba')
            
            #if not verificaCPF(cpf1):
            #    messages.error(request, 'CPF Inválido')
            #    return redirect('cadastro_baba') 

            if not cpf.validate(cpf1):
                messages.error(request, 'CPF Inválido')
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
                email=email1,
                nome=nome1,
                cpf=cpf1,
                nascimento=nascimento1,
                telefone= telefone1,
                endereco=endereco1
            )
            print('banana')
            usuario.set_password(senha1)
            usuario.isBaba = True
            usuario.save()
            usuario.updateSlug()
            usuario.save()
            messages.success(request, 'Cadastro efetuado com sucesso!')
            return redirect('login')

    return render(request, 'users/register_baba.html', {'form': form})

def cadastro_responsavel(request):
    form = CadastroFormsResponsavel()
    cpf = CPF()

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
        
            
            if not verificar_registros_mx(email1):
                messages.error(request, 'O domínio do e-mail não é válido ou não aceita mensagens.')
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
            
            #idade
            nascimento_str = request.POST.get('nascimento')  
            try:
                nascimento1 = datetime.strptime(nascimento_str, '%Y-%m-%d').date() 
            except (ValueError, TypeError):
                messages.error(request, 'Data de nascimento inválida. Use o formato AAAA-MM-DD.')
                return redirect('cadastro_baba')

            # Calcula a idade
            hoje = timezone.now().date()
            idade = hoje.year - nascimento1.year - ((hoje.month, hoje.day) < (nascimento1.month, nascimento1.day))

            if idade < 18:
                messages.error(request, 'Faixa etária não permitida.')
                return redirect('cadastro_baba')
            
            if not cpf.validate(cpf1):
                messages.error(request, 'CPF Inválido')
                return redirect('cadastro_baba') 

            usuario = Responsavel.objects.create(
                email=email1,
                nome=nome1,
                cpf=cpf1,
                nascimento=nascimento1,
                telefone= telefone1,
                endereco=endereco1
            )
            print('banana responsavel')
            usuario.set_password(senha1)
            usuario.isBaba = False
            usuario.save()
            usuario.updateSlug()
            usuario.save()
            messages.success(request, 'Cadastro efetuado com sucesso!')
            return redirect('login')

    return render(request, 'users/register_responsavel.html', {'form': form})

'''def verificaCPF(cpf):
    i = 1
    sum = 0
    digit1: int
    digit2: int
    for x in cpf:
        if i == 10: break
        sum = sum + (i * (ord(x) - ord('0')))
        i = i + 1
    digit1 = sum % 11
    sum = 0
    i = 0
    for x in cpf:
        if i == 10: break
        sum = sum + (i * (ord(x) - ord('0')))
        i = i + 1
    digit2 = sum % 11
    if (digit1 == 10): digit1 = 0
    if (digit2 == 10): digit2 = 0
    if (chr(digit1 + ord('0')) == cpf[-2] and chr(digit2 + ord('0')) == cpf[-1]): return True
    else: return False'''
    
def verificar_registros_mx(email):
    try:
        dominio = email.split('@')[-1]  
        mx_records = dns.resolver.resolve(dominio, 'MX')
        return True if mx_records else False
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
        return False