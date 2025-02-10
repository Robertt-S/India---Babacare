from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from users.models import Baba
from perfis.models import Agenda

class Command(BaseCommand):
    help = "Preenche as agendas das babás para as próximas duas semanas (segunda a sexta, de manhã, recorrente)."

    def handle(self, *args, **options):
        hoje = datetime.today().date()
        inicio_recorrencia = hoje
        fim_recorrencia = hoje + timedelta(weeks=2)

        dias_da_semana = {
            0: "Segunda-feira",
            1: "Terça-feira",
            2: "Quarta-feira",
            3: "Quinta-feira",
            4: "Sexta-feira",
        }

        babas = Baba.objects.all()

        for baba in babas:
            dia_atual = inicio_recorrencia
            frequencias = []  # Lista para armazenar os dias da semana recorrentes

            while dia_atual <= fim_recorrencia:
                if dia_atual.weekday() in dias_da_semana:  # Verifica se é de segunda a sexta
                    dia_nome = dias_da_semana[dia_atual.weekday()]  # Nome do dia

                    # 🔍 Verifica se já existe esse registro para a baba
                    if not Agenda.objects.filter(baba=baba, dia=dia_atual, periodo="manhã").exists():
                        Agenda.objects.create(
                            baba=baba,
                            dia=dia_atual,
                            periodo="manhã",
                            disponibilidade=True,
                            recorrente=True,
                            frequencia=dia_nome,  # Armazena o nome correto do dia
                            inicio_recorrencia=inicio_recorrencia,
                            fim_recorrencia=fim_recorrencia
                        )
                    
                    # Adiciona o nome do dia à lista (para a primeira inserção)
                    if dia_nome not in frequencias:
                        frequencias.append(dia_nome)

                dia_atual += timedelta(days=1)  # Avança para o próximo dia
            
            # Atualiza os registros criados para manter a formatação correta na frequência
            Agenda.objects.filter(
                baba=baba,
                inicio_recorrencia=inicio_recorrencia,
                fim_recorrencia=fim_recorrencia
            ).update(frequencia=",".join(frequencias))

        self.stdout.write(self.style.SUCCESS("Agendas preenchidas com sucesso!"))
