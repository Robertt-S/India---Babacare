# Generated by Django 5.1.3 on 2025-02-07 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_alter_feedback_contract'),
        ('perfis', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Servico',
        ),
    ]
