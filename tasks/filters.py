import django_filters
from .models import Task
from statuses.models import Status
from labels.models import Label
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(queryset=Status.objects.all(), label='Status')
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all(), label='Author')
    labels = django_filters.ModelChoiceFilter(queryset=Label.objects.all(), label='Label')

    class Meta:
        model = Task
        fields = ['status', 'author', 'labels']