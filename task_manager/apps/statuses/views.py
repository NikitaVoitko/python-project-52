from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models.deletion import ProtectedError
from .models import Status
from task_manager.mixins import DeleteProtectionMixin, AuthRequiredMixin


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    template_name = 'statuses/status_form.html'
    fields = ['name']
    success_url = reverse_lazy('status-list')

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно создан')
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    template_name = 'statuses/status_form.html'
    fields = ['name']
    success_url = reverse_lazy('status-list')

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно изменен')
        return super().form_valid(form)

class StatusDeleteView(DeleteProtectionMixin,
                       AuthRequiredMixin,
                       DeleteView):

    login_url = reverse_lazy('login')
    success_message = ('Статус успешно удален')
    success_url = reverse_lazy('status-list')
    template_name = 'statuses/status_confirm_delete.html'
    model = Status
    protected_url = reverse_lazy('status-list')
    protected_message = ('Невозможно удалить статус, потому что он используется')

