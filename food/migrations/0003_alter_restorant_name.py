# Generated by Django 4.2 on 2025-03-21 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restorant',
            name='name',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
