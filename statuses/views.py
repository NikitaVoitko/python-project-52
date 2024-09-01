from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Status


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
        messages.success(self.request, 'Status created successfully.')
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    template_name = 'statuses/status_form.html'
    fields = ['name']
    success_url = reverse_lazy('status-list')

    def form_valid(self, form):
        messages.success(self.request, 'Status updated successfully.')
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_confirm_delete.html'
    success_url = reverse_lazy('status-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Status deleted successfully.')
        return super().delete(request, *args, **kwargs)
