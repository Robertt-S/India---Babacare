# Generated by Django 5.1.3 on 2024-12-07 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_baseuser_isbaba'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='numero',
            field=models.TextField(blank=True, null=True),
        ),
    ]
