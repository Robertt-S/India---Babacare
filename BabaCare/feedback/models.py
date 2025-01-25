from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Feedback(models.Model):
    #contract = models.ForeignKey(Contrato, on_delete=models.CASCADE) -> vai ser a chave primária e estrangeira, mas precisa do contrato pronto
    title = models.CharField(max_length=100, blank=False)
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    description = models.TextField(max_length=500)