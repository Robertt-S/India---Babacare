# Generated by Django 5.1.2 on 2024-11-18 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Baba',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('cpf', models.CharField(max_length=11, unique=True)),
                ('data_nascimento', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('senha', models.CharField(max_length=128)),
                ('numero_celular', models.CharField(max_length=15, unique=True)),
                ('endereco', models.TextField()),
                ('descricao', models.TextField()),
                ('foto', models.ImageField(blank=True, upload_to='fotos/%Y/%m/%d/')),
                ('verificado', models.BooleanField(default=False)),
            ],
        ),
    ]
