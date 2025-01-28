from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from perfis.models import Servico

class Feedback(models.Model):
    contract = models.ForeignKey(Servico, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    description = models.TextField(max_length=500)
    REQUIRED_FIELDS = ["title", "score", "description"]