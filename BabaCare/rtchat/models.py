from users.models import BaseUser
from django.db import models
from users.models import Baba, Responsavel

class Mensagem(models.Model):
    baba = models.ForeignKey(Baba, on_delete=models.CASCADE, related_name='mensagens_baba')  # Adicionado related_name
    responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE, related_name='mensagens_responsavel')  # Adicionado related_name
    autor = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='mensagens_autor')  # Adicionado related_name
    conteudo = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.autor.username}: {self.conteudo[:20]}"