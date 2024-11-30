from django.db import models
from datetime import date
from django.core.validators import EmailValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from autoslug import AutoSlugField

class UserManager(BaseUserManager):
    def create_user(self, email, nome, cpf, nascimento, telefone, endereco, password=None):
        if not email:
            raise ValueError("Usuários devem possuir um email")
        
        user = self.model(
            email=self.normalize_email(email),
            nome=nome,
            cpf=cpf,
            nascimento=nascimento,
            telefone=telefone,
            endereco=endereco
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, nome, cpf, nascimento, telefone, endereco, password=None):
        if not email:
            raise ValueError("Usuários devem possuir um email")
        
        user = self.model(
            email=self.normalize_email(email),
            nome=nome,
            cpf=cpf,
            nascimento=nascimento,
            telefone=telefone,
            endereco=endereco
        )

        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class BaseUser(AbstractBaseUser):
    
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, null=False, blank=False)
    cpf = models.CharField(max_length=11, unique=True)  
    nascimento = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True, validators=[EmailValidator()])  
    telefone = models.CharField(max_length=15)   
    endereco = models.TextField()  
    foto = models.ImageField(upload_to="fotos/%Y/%m/%d/", blank=True)
    criado = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(populate_from='nome',unique_with=['id'])
    isBaba = models.BooleanField(null=True, blank=True)
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["nome", "cpf", "nascimento", "telefone", "endereco"]
    
    objects = UserManager()

    def updateSlug(self):
        self.slug = f"{self.slug}-{self.id}"

    def idade(self):
        if self.nascimento:
            hoje = date.today()
            return hoje.year - self.nascimento.year - (
                (hoje.month, hoje.day) < (self.nascimento.month, self.nascimento.day)
            )
        return None

class Baba(BaseUser):
    
    bioBaba = models.TextField(null=False, blank=False)
    habilidades = models.TextField(max_length=255,default="")
    isBaba = True

    class Meta:
        db_table = 'users_babas'  
        verbose_name = 'Babá'
        verbose_name_plural = 'Babás'
        
    def __str__(self):
        return self.nome
    
    
class Responsavel(BaseUser):
    
    bioResp = models.TextField(null=False, blank=False)
    isBaba = False
    
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
        return self.id
