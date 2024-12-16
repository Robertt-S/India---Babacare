from django.db import models
from django.conf import settings
from autoslug import AutoSlugField
from django.conf import settings

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
    foto = models.ImageField(blank=False,upload_to="images/",default='')
    
    def __str__(self):
        return self.nome_completo
    
class Agenda(models.Model):
    baba = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL
    dia = models.DateField()  # Data disponível
    periodo = models.CharField(max_length=20, choices=[
        ('manhã', 'Manhã'),
        ('tarde', 'Tarde'),
        ('noite', 'Noite'),
        ('integral', 'Integral'),
    ])
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