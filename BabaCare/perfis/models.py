from django.db import models
from django.conf import settings
from autoslug import AutoSlugField
from django.conf import settings
from django.utils.timezone import now
from users.models import Baba, Responsavel

# Create your models here.

#No exemplo do codemy.com youtube, seria o event model
class Perfil_Baba(models.Model):
    # saber de quem é página, deleta o perfil de baba junto com o user
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=255)
    data_nascimento = models.DateField(blank=True)
    email = models.EmailField(max_length=255,blank=False)
    contato = models.CharField(max_length=255,default="")
    endereco = models.CharField(max_length=255)
    cpf = models.CharField(max_length=255, unique=True,blank=False)
    link = models.CharField(max_length=50,blank=True)
    slug = AutoSlugField(populate_from='link',unique_with=('cpf', 'email','owner'))
    habilidades = models.TextField(max_length=255,default="")
    foto = models.ImageField(blank=False,upload_to="images/",default='../static/images/white-square.png')
    
    def __str__(self):
        return self.nome_completo
    
class Agenda(models.Model):
    baba = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL
    dia = models.DateField()  # Data disponível
    periodo = models.CharField(max_length=20, choices=[
        ('manhã', 'Manhã'),
        ('tarde', 'Tarde'),
        ('noite', 'Noite'),
    ])
    disponibilidade = models.BooleanField(default=True)
    recorrente = models.BooleanField(default=False)  # Se for recorrente ou não
    frequencia = models.CharField(max_length=20, blank=True, null=True)  # Ex: "Segunda-feira"
    inicio_recorrencia = models.DateField(blank=True, null=True)  # Data de início da recorrência
    fim_recorrencia = models.DateField(blank=True, null=True)  # Data de término da recorrência

    class Meta:
        unique_together = ('baba', 'dia', 'periodo')       
        
class Perfil_Resp(models.Model):
    # saber de quem é página, deleta o perfil do resp junto com o user
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=255)
    data_nascimento = models.DateField(blank=True)
    email = models.EmailField(max_length=255,blank=False)
    contato = models.CharField(max_length=255,default="")
    endereco = models.CharField(max_length=255)
    cpf = models.CharField(max_length=255, unique=True,blank=False)
    link = models.CharField(max_length=50,blank=True)
    slug = AutoSlugField(populate_from='link',unique_with=('cpf', 'email','owner'))
    foto = models.ImageField(blank=False,upload_to="images/")
    
    def __str__(self):
        return self.nome_completo
    
# class Servico(models.Model):
#     PERIODOS = [
#         ('manha', 'Manhã'),
#         ('tarde', 'Tarde'),
#         ('noite', 'Noite'),
#     ]

#     baba = models.ForeignKey(Baba, on_delete=models.CASCADE, related_name='servicos')
#     contratante = models.ForeignKey(Responsavel, on_delete=models.CASCADE, related_name='contratacoes')
#     nome_responsavel = models.CharField(max_length=100, blank=True)  # Novo campo
#     data_contratacao = models.DateTimeField(default=now)
#     data_servico = models.DateField()
#     periodo = models.CharField(max_length=10, choices=PERIODOS)
#     status = models.CharField(
#         max_length=20,
#         choices=[
#             ('pendente', 'Pendente'),
#             ('confirmado', 'Confirmado'),
#             ('cancelado', 'Cancelado'),
#         ],
#         default='pendente'
#     )

#     def save(self, *args, **kwargs):
#         # Preenche automaticamente o nome do responsável
#         if self.contratante:
#             self.nome_responsavel = self.contratante.nome
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Serviço ({self.periodo}) de {self.baba.usuario.username} para {self.contratante.usuario.username} em {self.data_servico}"
