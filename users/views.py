from django.shortcuts import render
from .models import Baba, Responsavel


def CadastroDaBaba(request):
    return render(request,'users/CadastroDaBaba.html')

def CadastroDoResponsavel(request):
    return render(request,'users/CadastroDoResponsavel.html')

def Responsaveis(request):
    
    # Salvando responsaveis
    novo_responsavel = Responsavel()
    novo_responsavel.nome = request.POST.get('nome')
    novo_responsavel.email = request.POST.get('email')
    novo_responsavel.cpf = request.POST.get('cpf')
    novo_responsavel.save()
    
    # Plot Reesponsaveis
    
    responsaveis = {
        
        'responsaveis': Responsavel.objects.all()
        
    }
    
    return render(request,'users/lista_responsaveis.html',responsaveis)


def Babas(request):
    
    # Salva baba
    nova_baba = Baba()
    nova_baba.nome = request.POST.get('nome')
    nova_baba.email = request.POST.get('email')
    nova_baba.cpf = request.POST.get('cpf')
    nova_baba.save()
    
    # Plot Baba
    babas = {
        
        'babas': Baba.objects.all()
        
    }
    
    return render(request,'users/lista_babas.html',babas)