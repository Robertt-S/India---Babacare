from django.shortcuts import render, redirect
from users.models import Baba as Perfil_Baba
from users.models import Responsavel as Perfil_Responsavel
from .forms import EditBabaForm, EditRespForm, AgendaRecorrenteForm
from datetime import datetime, timedelta
from datetime import date
import calendar
from calendar import monthrange
from .models import Agenda
from django.contrib import messages
from collections import defaultdict
from math import radians, sin, cos, acos
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ContratacaoForm
from .models import Baba, Servico
from django.utils.timezone import now
from django.urls import reverse
# Create your views here.

# Só responsáveis usam esse view
def baba_list(request):
    perfil_responsavel = request.user  
    users = []
    data_servico = None
    periodo = None
    lista_pBabas= []
    if request.method == 'POST':
        form = ContratacaoForm(request.POST)
        if form.is_valid():
            data_servico = form.cleaned_data['data_servico']
            periodo = form.cleaned_data['periodo']
            
            #
            agendas_disponiveis = Agenda.objects.filter(dia=data_servico, periodo=periodo, disponibilidade=True)
            
            for agenda in agendas_disponiveis:
                baba = agenda.baba
                users.append(baba)
                
                # passando o perfil para pega a biografia da baba
                perfil_baba = Perfil_Baba.objects.get(pk=baba)
                
                if dentro_do_raio(perfil_baba.lat, perfil_baba.long, perfil_responsavel.lat, perfil_responsavel.long, perfil_baba.rangeTrabalho):
                    lista_pBabas.append(perfil_baba)

    else:
        form = ContratacaoForm()  # Formulário vazio para GET

    return render(request, 'perfis/baba_list.html', {'users': users, 'form': form, 'data_servico': data_servico, 'periodo': periodo, 'lista_pBabas':lista_pBabas})

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
    agendas = Agenda.objects.filter(dia__year=ano, dia__month=mes)  # Filtra pelas datas do mês
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


@login_required
def contratar_servico(request, id):
    # Carrega a babá pela ID
    baba = get_object_or_404(Perfil_Baba, id=id)

    if request.method == 'POST':
        # Obtém os dados enviados via POST
        data_servico = request.POST.get('data_servico')
        periodo = request.POST.get('periodo')

        if data_servico and periodo:  # Garante que os dados foram enviados
            responsavel = get_object_or_404(Perfil_Responsavel, email=request.user.email)
            data_contratacao = now()  # Data atual da contratação
            
            data_servico = datetime.strptime(data_servico, "%d/%m/%Y").date()
            # Cria o serviço com os dados fornecidos
            Servico.objects.create(
                baba=baba,
                contratante=responsavel,
                data_servico=data_servico,
                periodo=periodo,
                data_contratacao=data_contratacao
            )

            # Exibe mensagem de sucesso e redireciona para a página inicial
            messages.success(request, 'Contrato de serviço solicitado com sucesso!')
            return redirect('home')  # Redireciona para uma página existente, ajuste conforme necessário
        else:
            messages.error(request, 'Os dados de data ou período não foram fornecidos.')
            return redirect('perfis:lista_babas')  # Redireciona para a lista de babás, ajuste conforme necessário

    # Renderiza a página com os detalhes da babá
    return render(request, 'perfis/contratar_servico.html', {'baba': baba})


###--- Funções de utilidade ---###

def distancia_em_km(lat1, lon1, lat2, lon2):
    raio_terra = 6371

    return raio_terra * acos(sin(radians(lat1)) * sin(radians(lat2)) +
                             cos(radians(lat1)) * cos(radians(lat2)) *
                             cos(radians(lon1) - radians(lon2)))

def dentro_do_raio(lat_baba, long_baba, lat_responsavel, long_responsavel, raio):
    return distancia_em_km(lat_baba, long_baba, lat_responsavel, long_responsavel) <= raio


@login_required
def gerenciar_servicos(request):
    baba = request.user  # Babá autenticada
    if not baba.isBaba:  # Verifica se o usuário é uma babá
        return redirect('home')

    # Filtra os serviços pendentes e confirmados
    servicos_pendentes = Servico.objects.filter(baba=baba, status='pendente').order_by('-data_contratacao')
    servicos_confirmados = Servico.objects.filter(baba=baba, status='confirmado').order_by('-data_contratacao')
    
    if request.method == 'POST':
        # Ações para aceitar ou negar um serviço
        servico_id = request.POST.get('servico_id')
        acao = request.POST.get('acao')
        servico = get_object_or_404(Servico, id=servico_id, baba=baba)
        
        if acao == 'aceitar':
            # Busca a agenda correspondente
            agenda = Agenda.objects.filter(
                baba=baba,
                dia=servico.data_servico,
                periodo=servico.periodo
            ).first()
            
            if agenda and agenda.disponibilidade:
                # Atualiza o status do serviço para confirmado
                servico.status = 'confirmado'
                servico.save()

                # Atualiza a disponibilidade da agenda
                agenda.disponibilidade = False
                agenda.save()

                messages.success(
                    request, f"Serviço no dia {servico.data_servico} foi aceito e a disponibilidade da agenda foi atualizada."
                )
            else:
                # Agenda indisponível ou inexistente
                servico.status = 'cancelado'
                servico.save()
                
                messages.success(
                    request, f"Serviço no dia {servico.data_servico} foi cancelado, pois a agenda não está disponível ou já foi preenchida. Verifique sua agenda."
                )

        elif acao == 'negar':
            # Negar o serviço
            servico.status = 'cancelado'
            servico.save()
            
            messages.success(
                request, f"Serviço no dia {servico.data_servico} foi negado."
            )

        return redirect('perfis:gerenciar_servicos')  # Nome da URL configurada no projeto

    return render(request, 'perfis/gerenciar_servicos.html', {
        'servicos_pendentes': servicos_pendentes,
        'servicos_confirmados': servicos_confirmados,
    })
    
@login_required
def servicos_responsavel(request):
    
    responsavel = get_object_or_404(Perfil_Responsavel, email=request.user.email)

    
    servicos_solicitados = Servico.objects.filter(contratante=responsavel).order_by('-data_contratacao')

    
    return render(request, 'perfis/servicos_responsavel.html', {
        'servicos_solicitados': servicos_solicitados,
    })