from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.ForeignKey('statuses.Status', on_delete=models.PROTECT)
    executor = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True) 
    labels = models.ManyToManyField('labels.Label', related_name='tasks_with_labels', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_created', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name