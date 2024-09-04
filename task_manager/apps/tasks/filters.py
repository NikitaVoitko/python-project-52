import django_filters
from .models import Task
from task_manager.apps.statuses.models import Status
from task_manager.apps.labels.models import Label
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(queryset=Status.objects.all(), label='Статус')
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all(), label='Автор')
    executor = django_filters.ModelChoiceFilter(queryset=User.objects.all(), label='Исполнитель')
    labels = django_filters.ModelMultipleChoiceFilter(queryset=Label.objects.all(), label='Метки')
    own_tasks = django_filters.BooleanFilter(method='filter_own_tasks', label='Только свои задачи')

    def filter_own_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'author', 'executor', 'labels', 'own_tasks']
