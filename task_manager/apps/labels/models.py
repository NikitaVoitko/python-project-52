from django.db import models
from django.core.exceptions import ValidationError


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)
    tasks = models.ManyToManyField('tasks.Task', related_name='tasks_with_labels', blank=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.tasks.exists():
            raise ValidationError("Cannot delete label that is assigned to a task.")
        super().delete(*args, **kwargs)
