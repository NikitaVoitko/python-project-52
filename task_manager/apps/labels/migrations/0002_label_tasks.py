# Generated by Django 5.1 on 2024-09-03 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='tasks',
            field=models.ManyToManyField(blank=True, related_name='tasks_with_labels', to='tasks.task'),
        ),
    ]
