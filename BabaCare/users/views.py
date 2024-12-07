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
import requests



def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if user.isBaba == True:
                return redirect('users:home_baba')
            else:
                return redirect('users:home_responsavel')
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
            numero1=form['numero'].value()
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

            # Cálculo da Latitude e Longitude
            tupla_lat_lon = coordenadasCep(endereco1, numero1)
            lat1, long1 = tupla_lat_lon

            usuario = Baba.objects.create(
                email=email1,
                nome=nome1,
                cpf=cpf1,
                nascimento=nascimento1,
                telefone= telefone1,
                endereco=endereco1,
                numero=numero1,
                lat=lat1,
                long=long1
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
            numero1=form['numero'].value()
            nascimento1=form['nascimento'].value()
            cpf1=form['cpf'].value()

            if form["senha_1"].value() != form["senha_2"].value():
                messages.error(request, 'Senhas não são iguais')
                return redirect('cadastro_responsavel')
        
            
            # if not verificar_registros_mx(email1):
            #     messages.error(request, 'O domínio do e-mail não é válido ou não aceita mensagens.')
            #     return redirect('cadastro_responsavel')
        
            
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

        
            # Cálculo da Latitude e Longitude    
            tupla_lat_lon = coordenadasCep(endereco1, numero1)
            lat1, long1 = tupla_lat_lon


            usuario = Responsavel.objects.create(
                email=email1,
                nome=nome1,
                cpf=cpf1,
                nascimento=nascimento1,
                telefone= telefone1,
                endereco=endereco1,
                numero=numero1,
                lat=lat1,
                long=long1
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
    
def home_baba(request):
    return render(request, 'users/home_baba.html')
    
def home_responsavel(request):
    return render(request,'users/home_responsavel.html')


def consultaViacep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "erro" not in data:
            return data  # Retorna os dados do endereço
        else:
            return None  # CEP não encontrado
    else:
        return None  # Erro na requisição
     
def coordGoogleMaps(endereco, numero, google_api_key):
    # Formatação do endereço para API do Google
    endereco_completo = f"{numero} {endereco['logradouro']}, {endereco['localidade']}, {endereco['uf']}, {endereco['cep']}, Brazil"
    
    # URL da Google Geocoding API
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    
    # Parâmetros passados
    params = {
        "address": endereco_completo,
        "key": google_api_key
    }
    
    # Faz a requisição
    response = requests.get(url, params=params)
    
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            # Obtém a latitude e longitude do primeiro resultado
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
        else:
            return "Endereço não encontrado."
    else:
        return f"Erro na requisição: {response.status_code}"
    
def coordenadasCep(cep, numero):
    # Consultar ViaCEP para obter o endereço completo
    endereco = consultaViacep(cep)
    
    if endereco:
        # Obter latitude e longitude com o Google Maps API
        lat_lon = coordGoogleMaps(endereco, numero, "INSIRA_SUA_KEY_AQUI") # <--------------------------------- INSERIR KEY DO GOOGLE MAPS API
        return lat_lon
    else:
        return "CEP não encontrado."

