from django.db import models
from users.models import BaseUser

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content}'