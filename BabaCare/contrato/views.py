from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.utils import timezone

from users.models import Baba as Perfil_Baba, Responsavel
from users.models import Responsavel as Perfil_Responsavel
from .models import Servico
from perfis.models import Agenda
from .forms import ContratacaoForm

from datetime import datetime

from huggingface_hub import InferenceClient
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from math import radians, sin, cos, acos


def baba_list(request):
    base_user_responsavel = request.user
    perfil_responsavel = Perfil_Responsavel.objects.get(id=base_user_responsavel.id)
    perfis_babas = []
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
                perfil_baba = Perfil_Baba.objects.get(pk=baba.pk)
                if dentro_do_raio(perfil_baba.lat, perfil_baba.long, base_user_responsavel.lat, base_user_responsavel.long, perfil_baba.rangeTrabalho):
                    perfis_babas.append(perfil_baba)

            
            perfis_babas = ordenar_babas_por_similaridade(perfil_responsavel, perfis_babas)
            # messages.info(request, f"users_ordenado: {users[1]}")
            
    else:
        form = ContratacaoForm()  # Formulário vazio para GET


    return render(request, 'contrato/baba_list.html', {
        'perfis': perfis_babas,
        'form': form,
        'data_servico': data_servico,
        'periodo': periodo,
    })
    
@login_required
def contratar_servico(request, id):
    # Carrega a babá pela ID
    baba = get_object_or_404(Perfil_Baba, id=id)

    if request.method == 'POST':
        # Obtém os dados enviados via POST
        data_servico = request.POST.get('data_servico')  # Formato recebido: YYYY-MM-DD
        periodo = request.POST.get('periodo')

        if data_servico and periodo:  # Garante que os dados foram enviados
            responsavel = get_object_or_404(Perfil_Responsavel, email=request.user.email)
            data_contratacao = now()  # Data atual da contratação

            try:
                data_servico = datetime.strptime(data_servico, "%Y-%m-%d").date()  # Correção do formato
            except ValueError:
                messages.error(request, 'Formato de data inválido. Use o calendário do formulário.')
                return redirect('contrato:lista_babas')

            # Cria o serviço com os dados fornecidos
            Servico.objects.create(
                baba=baba,
                contratante=responsavel,
                data_servico=data_servico,
                periodo=periodo,
                data_contratacao=data_contratacao
            )

            messages.success(request, 'Contrato de serviço solicitado com sucesso!')
            return redirect('home')  # Redireciona para a página inicial
        else:
            messages.error(request, 'Os dados de data ou período não foram fornecidos.')
            return redirect('contrato:lista_babas')  # Redireciona para a lista de babás

    # Renderiza a página com os detalhes da babá
    return render(request, 'contrato/contratar_servico.html', {'baba': baba})


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

        return redirect('contrato:gerenciar_servicos')  # Nome da URL configurada no projeto

    return render(request, 'contrato/gerenciar_servicos.html', {
        'servicos_pendentes': servicos_pendentes,
        'servicos_confirmados': servicos_confirmados,
    })


@login_required
def servicos_responsavel(request):
    
    responsavel = get_object_or_404(Responsavel, email=request.user.email)

    
    # servicos_solicitados = Servico.objects.filter(contratante=responsavel).order_by('-data_contratacao')
    servicos_solicitados = Servico.objects.filter(contratante=responsavel).select_related('baba').order_by('-data_contratacao')
    
    return render(request, 'contrato/servicos_responsavel.html', {
        'servicos_solicitados': servicos_solicitados,
        'today': timezone.now().date(),
    })

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
    

def ordenar_babas_por_similaridade(perfil_responsavel, perfis_babas):
    similaridades = perfil_responsavel.babasSimilares

    perfis_babas = sorted(perfis_babas, key=lambda baba: similaridades[str(baba.id)] if str(baba.id) in similaridades else 0, reverse=True)

    return perfis_babas