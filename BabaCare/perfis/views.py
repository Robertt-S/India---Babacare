from django.shortcuts import render, redirect
from users.models import Baba as Perfil_Baba
from users.models import Responsavel as Perfil_Responsavel
from contrato.forms import ContratacaoForm
from .forms import EditBabaForm, EditRespForm, AgendaRecorrenteForm
from datetime import datetime, timedelta

import calendar
from calendar import monthrange
from .models import Agenda
from django.contrib import messages
from collections import defaultdict
from math import radians, sin, cos, acos
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


from django.utils.timezone import now

from django.urls import reverse

from huggingface_hub import InferenceClient
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def baba_list(request):
    base_user_responsavel = request.user
    perfil_responsavel = Perfil_Responsavel.objects.get(id=base_user_responsavel.id)
    users = set()  # Usando um set para evitar duplicatas
    perfilBabas_dict = {}  # Novo dicionário para associar babás aos seus perfis
    data_servico = None
    periodo = None


    if request.method == 'POST':
        form = ContratacaoForm(request.POST)
        if form.is_valid():
            data_servico = form.cleaned_data['data_servico']
            periodo = form.cleaned_data['periodo']

            # Busca agendas disponíveis no dia e período escolhidos
            agendas_disponiveis = Agenda.objects.filter(dia=data_servico, periodo=periodo, disponibilidade=True)

            for agenda in agendas_disponiveis:
                baba = agenda.baba

                if baba not in users:  # Evita duplicação
                    perfil_baba = Perfil_Baba.objects.get(pk=baba.pk)
                    if dentro_do_raio(perfil_baba.lat, perfil_baba.long, base_user_responsavel.lat, base_user_responsavel.long, perfil_baba.rangeTrabalho):
                        users.add(baba)
                        perfilBabas_dict[baba.id] = perfil_baba  # Adiciona ao dicionário
    else:
        form = ContratacaoForm()  # Formulário vazio para GET

    users, perfilBabas_dict = ordenar_babas_por_similaridade(perfil_responsavel, list(users), perfilBabas_dict)

    return render(request, 'perfis/baba_list.html', {
        'users': users,  # Converte set para lista antes de passar ao template
        'form': form,
        'data_servico': data_servico,
        'periodo': periodo,
        'perfilBabas_dict': perfilBabas_dict  # Passa o dicionário atualizado
    })


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


###--- Classes e Funções de utilidade ---###

def distancia_em_km(lat1, lon1, lat2, lon2):
    raio_terra = 6371

    return raio_terra * acos(sin(radians(lat1)) * sin(radians(lat2)) +
                             cos(radians(lat1)) * cos(radians(lat2)) *
                             cos(radians(lon1) - radians(lon2)))

def dentro_do_raio(lat_baba, long_baba, lat_responsavel, long_responsavel, raio):
    return distancia_em_km(lat_baba, long_baba, lat_responsavel, long_responsavel) <= raio




class SentenceSimilarityWithAPI():
    def __init__(self, model_name: str):
        self.client = InferenceClient(model_name)

    def sentence_similarity(self, sentence: str, other_sentences: list[str]) -> list[float]:
        return self.client.sentence_similarity(sentence, other_sentences)


class SentenceSimilarityWithLocalModel():
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def sentence_similarity(self, sentence: str, other_sentences: list[str]) -> list[float]:
        embeddings = self.model.encode([sentence] + other_sentences)
        similarity = cosine_similarity(embeddings)

        return similarity[0][1:]


class SentenceSimilarityAdapter():
    def __init__(self, model_name: str, use_api=True) -> None:
        if use_api:
            self.similarity_model = SentenceSimilarityWithAPI(model_name)
        else:
            self.similarity_model = SentenceSimilarityWithLocalModel(model_name)

    def sentence_similarity(self, sentence: str, other_sentences: list[str]) -> list[float]:
        return self.similarity_model.sentence_similarity(sentence, other_sentences)
    

def ordenar_babas_por_similaridade(perfil_responsavel, babas_users, perfilBabas_dict):
    similaridades = perfil_responsavel.babasSimilares

    # Ordena as babás por similaridade
    babas_users = sorted(babas_users, key=lambda baba: similaridades[str(baba.id)] if str(baba.id) in similaridades else 0, reverse=True)

    # Cria um novo dicionário ordenado
    perfilBabas_dict = {baba.id: perfilBabas_dict[baba.id] for baba in babas_users}

    return babas_users, perfilBabas_dict