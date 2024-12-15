from django.shortcuts import render, redirect
#from .models import Perfil_Baba
from users.models import Baba as Perfil_Baba
from users.models import Responsavel as Perfil_Responsavel
from .forms import EditBabaForm, EditRespForm
from .models import Agenda
from datetime import timedelta, datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from .forms import AgendaRecorrenteForm
from django.contrib import messages


# Create your views here.

def baba_list(request):
    perfis = Perfil_Baba.objects.all()
    return render(request, 'perfis/baba_list.html', {'perfis': perfis})

# passa o id do perfil também
def edit_page(request, perfil_id):
    isbaba = request.user.isBaba
    if isbaba:
        #vai ver na tabela de perfis e buscar aquela com pk igual a que a gente clica na pagina
        perfil = Perfil_Baba.objects.get(pk=perfil_id)
        #form para editar
        #instance=perfil, na hora de editar, ele mostra o texto que já está gravado no perfil
        form = EditBabaForm(data=(request.POST or None),files=(request.FILES or None), instance = perfil)
    else:
        perfil = Perfil_Responsavel.objects.get(pk=perfil_id)
        form = EditRespForm(data=(request.POST or None),files=(request.FILES or None), instance = perfil)
    if form.is_valid():
        form.save()
        return redirect('perfis:my_page')
    
    return render(request, 'perfis/edit_page.html', {'perfil':perfil, 'form':form})

def my_page(request):
    if request.user.is_authenticated:
        eu_id = request.user.id
        isbaba = request.user.isBaba
        if isbaba: perfil = Perfil_Baba.objects.get(id=eu_id)
        else: perfil= Perfil_Responsavel.objects.get(id=eu_id)
        return render(request,'perfis/own_page.html',{'perfil': perfil,'eu_id':eu_id})

def page_baba(request,slug):
    perfilB = Perfil_Baba.objects.get(slug=slug) 
    #{'nome do conjunto de informações': informaçõesPassadas}
    return render(request, 'perfis/baba_page.html', {'perfilBaba': perfilB})

def agenda_recorrente(request):
    # Buscar o perfil do usuário logado
    perfil = request.user
    eu_id = perfil.id  # ID do perfil logado

    # Frequências fixas para a lógica do formulário
    FREQUENCIAS = [
        'Segunda-feira', 
        'Terça-feira', 
        'Quarta-feira', 
        'Quinta-feira', 
        'Sexta-feira',
        'Sábado',
        'Domingo'
    ]

    if request.method == 'POST':
        form = AgendaRecorrenteForm(request.POST)
        if form.is_valid():
            # Processar os dados do formulário
            periodo = form.cleaned_data['periodo']
            frequencia = form.cleaned_data['frequencia']
            inicio_recorrencia = form.cleaned_data['inicio_recorrencia']
            fim_recorrencia = form.cleaned_data['fim_recorrencia']

            baba = request.user  # Usuário logado (babá)
            data_atual = inicio_recorrencia
            data_ja_cadastrada = False  # Flag para indicar se já existe uma data cadastrada

            while data_atual <= fim_recorrencia:
                if FREQUENCIAS[data_atual.weekday()] in frequencia:
                    for p in periodo:
                        # Verificar se já existe uma agenda com a mesma data, período e babá
                        if Agenda.objects.filter(baba=baba, dia=data_atual, periodo=p).exists():
                            data_ja_cadastrada = True  # Se existir, marca a flag como True
                            break  # Não precisa continuar verificando

                        # Se não existir, cria a agenda
                        Agenda.objects.create(
                            baba=baba,
                            dia=data_atual,
                            periodo=p,
                            recorrente=True,
                            frequencia=','.join(frequencia),
                            inicio_recorrencia=inicio_recorrencia,
                            fim_recorrencia=fim_recorrencia
                        )
                if data_ja_cadastrada:
                    break  # Interrompe o loop se já encontrou a duplicação

                data_atual += timedelta(days=1)

            # Se uma data foi cadastrada, envia a mensagem de erro
            if data_ja_cadastrada:
                messages.error(request, "Data já cadastrada para este período.")

    else:
        form = AgendaRecorrenteForm()

    # Construir o contexto
    context = {
        'form': form,
        'perfil': perfil,
        'eu_id': eu_id,
    }

    return render(request, 'perfis/agenda_recorrente.html', context)

