# Generated by Django 2.0.8 on 2018-10-24 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admin',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='admin',
            name='sex',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='user',
            name='sex',
        ),
    ]
