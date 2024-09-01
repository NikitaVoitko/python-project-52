from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django_filters.views import FilterView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Task
from labels.models import Label
from .forms import TaskForm
from .filters import TaskFilter
from django.contrib.auth.models import User
from statuses.models import Status


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['users'] = User.objects.all()
        context['labels'] = Label.objects.all()
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tasks/task_form.html'
    form_class = TaskForm  # Используем кастомную форму TaskForm
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Task created successfully.')
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'
    form_class = TaskForm
    success_url = reverse_lazy('task-list')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author

    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully.')
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Task deleted successfully.')
        return super().delete(request, *args, **kwargs)