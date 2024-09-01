# Generated by Django 5.1 on 2024-09-01 11:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0002_remove_label_created_at_label_tasks'),
        ('statuses', '0001_initial'),
        ('tasks', '0002_remove_task_author_task_labels_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(blank=True, related_name='tasks_with_labels', to='labels.label'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='statuses.status'),
        ),
    ]
