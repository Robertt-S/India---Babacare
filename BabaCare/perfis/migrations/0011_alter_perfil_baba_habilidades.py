# Generated by Django 5.1.2 on 2024-11-07 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfis', '0010_perfil_baba_contato_perfil_baba_habilidades_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil_baba',
            name='habilidades',
            field=models.TextField(default='', max_length=255),
        ),
    ]