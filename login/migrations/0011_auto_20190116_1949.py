# Generated by Django 2.0.10 on 2019-01-16 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_auto_20190116_1810'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='label',
            name='task',
        ),
        migrations.RemoveField(
            model_name='task',
            name='users',
        ),
        migrations.AddField(
            model_name='subtask',
            name='num_tagged',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='subtask',
            name='users',
            field=models.ManyToManyField(related_name='tasks_owned', to='login.User'),
        ),
        migrations.AddField(
            model_name='task',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='max_num',
            field=models.IntegerField(default=1),
        ),
    ]
