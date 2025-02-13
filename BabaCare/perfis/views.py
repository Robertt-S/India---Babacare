from django.shortcuts import render, redirect
from django.contrib import messages
from collections import defaultdict
from django.shortcuts import render, redirect

from users.models import Baba as Perfil_Baba
from users.models import Responsavel as Perfil_Responsavel
from .models import Agenda
from .forms import EditBabaForm, EditRespForm, AgendaRecorrenteForm

from datetime import datetime, timedelta
import calendar




def buscar(request):
    perfis = Perfil_Baba.objects.all()

    if "buscar" in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            perfis = perfis.filter(nome__icontains=nome_a_buscar)

    return render(request, "perfis/buscar.html", {"perfis": perfis})

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


def gerar_calendario(ano, mes, request):
    # Validar o mês
    if not 1 <= mes <= 12:
        raise ValueError("Mês deve estar entre 1 e 12")

    eu_id = request.user.id

    # Calculando o primeiro dia do mês
    primeiro_dia = datetime(ano, mes, 1)
    dia_da_semana = primeiro_dia.weekday()  # 0 = segunda-feira, 6 = domingo

    # Obtendo os dias do mês
    dias_no_mes = calendar.monthrange(ano, mes)[1]
    
    # Gerar uma lista de dias do mês com os dias da semana corretamente posicionados
    calendario = [None] * dia_da_semana + list(range(1, dias_no_mes + 1))
    
    # Verificar as agendas da baba para o mês
    agendas = Agenda.objects.filter(baba_id=eu_id, dia__year=ano, dia__month=mes)

    # Criar um dicionário com os dias e turnos agendados
    agenda_por_dia = {}
    for agenda in agendas:
        if agenda.dia.day not in agenda_por_dia:
            agenda_por_dia[agenda.dia.day] = []
        agenda_por_dia[agenda.dia.day].append(agenda.periodo)

    return calendario, dia_da_semana


def agenda_recorrente(request):

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
                # Verifica se a data atual corresponde à frequência selecionada
                if FREQUENCIAS[data_atual.weekday()] in frequencia:
                    for p in periodo:
                        # Verificar se já existe uma agenda com a mesma data, período e babá
                        if Agenda.objects.filter(baba=baba, dia=data_atual, periodo=p).exists():
                            data_ja_cadastrada = True  # Marca que a data já está cadastrada
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
                    
                    if data_ja_cadastrada:  # Se alguma agenda já foi cadastrada, sai do loop
                        break  # Interrompe o loop principal, pois não deve continuar com as datas

                data_atual += timedelta(days=1)

            # Se uma data foi cadastrada, envia a mensagem de erro
            if data_ja_cadastrada:
                messages.error(request, "Data já cadastrada para este período.")

    else:
        form = AgendaRecorrenteForm()

    # Captura o mês e o ano da query string (ou usa o mês/ano atual como padrão)
    mes = int(request.GET.get('mes', datetime.now().month))
    ano = int(request.GET.get('ano', datetime.now().year))

    # Validar mês
    if not 1 <= mes <= 12:
        mes = datetime.now().month

    # Gerar o calendário
    calendario, dia_da_semana = gerar_calendario(ano, mes, request)

    # Coletar as agendas do banco de dados
    # agendas = Agenda.objects.filter(dia__year=ano, dia__month=mes)# # Filtra pelas datas do mês
    agendas = Agenda.objects.filter(baba=perfil, dia__year=ano, dia__month=mes)

    agendas_por_dia = defaultdict(list)
    
    dias_no_mes = len(calendario)
    dias_faltando = 7 - (dias_no_mes % 7) if dias_no_mes % 7 != 0 else 0

    # Criar uma lista de 'dias vazios' para o template
    dias_vazios = [None] * dias_faltando
    for agenda in agendas:
        agendas_por_dia[agenda.dia.day].append(agenda.periodo)

    context = {
        'calendario': calendario,
        'dia_da_semana': dia_da_semana,
        'mes': mes,
        'ano': ano,
        'agendas_por_dia': agendas_por_dia,  # Passa o dicionário de dias agendados
        'dias_da_semana': ["segunda", "terça", "quarta", "quinta", "sexta", "sabado", "domingo"],
        'meses': ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
        'anos': range(2023, 2031),
        'form': form,
        'perfil': perfil,
        'eu_id': eu_id,
        'dias_vazios': dias_vazios
    }

    return render(request, 'perfis/agenda_recorrente.html', context)