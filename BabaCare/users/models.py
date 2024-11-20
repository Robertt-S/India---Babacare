from django.db import models

from datetime import date



## Exemplo do GPT, deve ter algo melhor
# from django.core.exceptions import ValidationError
# def validar_cpf(cpf):
#     # Implementar lógica de validação de CPF aqui.
#     if len(cpf) != 11 or not cpf.isdigit():
#         raise ValidationError("CPF inválido")




class Baba(models.Model):

    
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, null=False, blank=False)
    cpf = models.CharField(max_length=11, unique=True)  
    data_nascimento = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)  
    senha = models.CharField(max_length=128)
    numero_celular = models.CharField(max_length=15, unique=True)   
    endereco = models.TextField()  
    descricao = models.TextField(null=False, blank=False)
    foto = models.ImageField(upload_to="fotos/%Y/%m/%d/", blank=True)
    verificado = models.BooleanField(default=False)
    

    def calcular_idade(self):
        if self.data_nascimento:
            hoje = date.today()
            return hoje.year - self.data_nascimento.year - (
                (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
            )
        return None


    def __str__(self):
        return self.nome
    
    
    
class Responsavel(models.Model):

    
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, null=False, blank=False)
    cpf = models.CharField(max_length=11, unique=True)  
    data_nascimento = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)  
    senha = models.CharField(max_length=128)
    numero_celular = models.CharField(max_length=15, unique=True)   
    endereco = models.TextField()  
    descricao = models.TextField(null=False, blank=False)
    foto = models.ImageField(upload_to="fotos/%Y/%m/%d/", blank=True)
    verificado = models.BooleanField(default=False)
    

    def calcular_idade(self):
        if self.data_nascimento:
            hoje = date.today()
            return hoje.year - self.data_nascimento.year - (
                (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
            )
        return None


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
        return self.comentario