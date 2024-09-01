# Generated by Django 5.1 on 2024-09-01 17:31

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_task_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
