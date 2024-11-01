from django.db import models

class Baba(models.Model):
    id_baba = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255)
    email = models.TextField(max_length=255)
    cpf = models.TextField(max_length=255)

class Responsavel(models.Model):
    id_responsavel = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255)
    email = models.TextField(max_length=255)
    cpf = models.TextField(max_length=255)



