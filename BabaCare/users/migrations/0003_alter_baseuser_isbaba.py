# Generated by Django 5.1.3 on 2024-11-30 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_baseuser_isbaba'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='isBaba',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
