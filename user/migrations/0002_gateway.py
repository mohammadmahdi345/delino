# Generated by Django 4.2 on 2025-03-21 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gateway',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('avatar', models.ImageField(blank=True, upload_to='pakages/', verbose_name='avatar')),
                ('is_enable', models.BooleanField(default=True, verbose_name='is_enable')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created_time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='updated_time')),
            ],
            options={
                'verbose_name': 'gateway',
                'verbose_name_plural': 'gateways',
                'db_table': 'gateway',
            },
        ),
    ]
