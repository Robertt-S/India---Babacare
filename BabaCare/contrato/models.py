from django.db import models
from django.utils.timezone import now
from users.models import Baba, Responsavel


# Create your models here.
class Servico(models.Model):
    PERIODOS = [
        ('manha', 'Manhã'),
        ('tarde', 'Tarde'),
        ('noite', 'Noite'),
    ]

    baba = models.ForeignKey(Baba, on_delete=models.CASCADE, related_name='servicos')
    contratante = models.ForeignKey(Responsavel, on_delete=models.CASCADE, related_name='contratacoes')
    nome_responsavel = models.CharField(max_length=100, blank=True)  # Novo campo
    data_contratacao = models.DateTimeField(default=now)
    data_servico = models.DateField()
    periodo = models.CharField(max_length=10, choices=PERIODOS)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pendente', 'Pendente'),
            ('confirmado', 'Confirmado'),
            ('cancelado', 'Cancelado'),
        ],
        default='pendente'
    )

    def save(self, *args, **kwargs):
        # Preenche automaticamente o nome do responsável
        if self.contratante:
            self.nome_responsavel = self.contratante.nome
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Serviço ({self.periodo}) de {self.baba.usuario.username} para {self.contratante.usuario.username} em {self.data_servico}"