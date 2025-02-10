from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from users.models import Baba, Responsavel
from perfis.models import Agenda
from contrato.models import Servico
from django.utils.timezone import now

class Command(BaseCommand):
    help = "Preenche agendas da semana passada e cria contratos confirmados."

    def handle(self, *args, **options):
        hoje = datetime.today().date()
        inicio_semana_passada = hoje - timedelta(days=hoje.weekday() + 7)
        fim_semana_passada = inicio_semana_passada + timedelta(days=4)

        dias_da_semana = {
            0: "Segunda-feira",
            1: "Terça-feira",
            2: "Quarta-feira",
            3: "Quinta-feira",
            4: "Sexta-feira",
        }

        babas = list(Baba.objects.all()[:3])  # Converte para lista para evitar consultas repetidas
        responsaveis = list(Responsavel.objects.all()[:2])  # Mesma otimização

        novas_agendas = []
        novos_servicos = []

        for baba in babas:
            frequencias = set()
            for i in range(3):  # Segunda a quarta
                dia_atual = inicio_semana_passada + timedelta(days=i)
                dia_nome = dias_da_semana.get(dia_atual.weekday())

                if not dia_nome:
                    continue  # Pula se não for um dia útil

                # Criar a agenda em memória
                agenda = Agenda(
                    baba=baba,
                    dia=dia_atual,
                    periodo="manhã",
                    disponibilidade=True,
                    recorrente=False,
                    frequencia=dia_nome,
                    inicio_recorrencia=None,
                    fim_recorrencia=None
                )
                novas_agendas.append(agenda)
                frequencias.add(dia_nome)

                # Criar contratos para os responsáveis
                for responsavel in responsaveis:
                    servico = Servico(
                        baba=baba,
                        contratante=responsavel,
                        data_servico=dia_atual,
                        periodo="manhã",
                        data_contratacao=now(),
                        status="confirmado"
                    )
                    novos_servicos.append(servico)

        # Salva as agendas e serviços de uma só vez
        if novas_agendas:
            Agenda.objects.bulk_create(novas_agendas)

        if novos_servicos:
            Servico.objects.bulk_create(novos_servicos)

        self.stdout.write(self.style.SUCCESS("Agendas e contratos criados com sucesso!"))
