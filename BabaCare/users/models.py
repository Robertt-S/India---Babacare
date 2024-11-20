from django.db import models

from datetime import date
from django.core.validators import EmailValidator



class BaseUser(models.Model):
    
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, null=False, blank=False)
    cpf = models.CharField(max_length=11, unique=True)  
    nascimento = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True, validators=[EmailValidator()])  
    senha = models.CharField(max_length=128)
    telefone = models.CharField(max_length=15)   
    endereco = models.TextField()  
    bio = models.TextField(null=False, blank=False)
    foto = models.ImageField(upload_to="fotos/%Y/%m/%d/", blank=True)
    criado = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True  # Class base abstrata
    
    def idade(self):
        if self.data_nascimento:
            hoje = date.today()
            return hoje.year - self.data_nascimento.year - (
                (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
            )
        return None




class Baba(BaseUser):
    class Meta:
        db_table = 'users_babas'  
        verbose_name = 'Babá'
        verbose_name_plural = 'Babás'
        
    def __str__(self):
        return self.nome
    
    
class Responsavel(BaseUser):
    class Meta:
        db_table = 'users_responsaveis'  
        verbose_name = 'Responsável'
        verbose_name_plural = 'Responsáveis'
        
    def __str__(self):
        return self.nome
    
class Avaliacao(models.Model):

    
    id = models.AutoField(primary_key=True)
    nota = models.IntegerField(blank=False, null=False)
    comentario = models.TextField(blank=True, null=True)
    data = models.DateField(auto_now=True)
    baba = models.ForeignKey(Baba, on_delete=models.CASCADE)
    responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.nome
