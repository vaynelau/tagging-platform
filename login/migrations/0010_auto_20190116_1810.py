# Generated by Django 2.0.10 on 2019-01-16 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_label_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='sub_task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='login.SubTask'),
        ),
        migrations.AlterField(
            model_name='label',
            name='task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='login.Task'),
        ),
    ]