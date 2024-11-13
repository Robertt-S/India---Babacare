# Generated by Django 5.1.2 on 2024-11-05 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil_baba',
            name='cpf',
            field=models.CharField(default='', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='perfil_baba',
            name='email',
            field=models.EmailField(max_length=255, unique=True),
        ),
    ]
