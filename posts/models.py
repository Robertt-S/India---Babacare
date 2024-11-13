from django.db import models

# Create your models here.
class Post(models.Model):
    #precisa ter tbsd
    title = models.CharField(max_length=75)     
    body = models.TextField()                   # text area input
    slug = models.SlugField() 
    date = models.DateTimeField(auto_now_add=True)  # date time is added every time a user post
    foto = models.ImageField(default='Sfoto.jpg', blank=True)
    
    def __str__(self):
        return self.title