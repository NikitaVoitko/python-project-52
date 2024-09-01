from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .models import Label

@method_decorator(login_required, name='dispatch')
class LabelListView(ListView):
    model = Label
    template_name = 'labels/label_list.html'

@method_decorator(login_required, name='dispatch')
class LabelCreateView(CreateView):
    model = Label
    fields = ['name']
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('label-list')

@method_decorator(login_required, name='dispatch')
class LabelUpdateView(UpdateView):
    model = Label
    fields = ['name']
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('label-list')

@method_decorator(login_required, name='dispatch')
class LabelDeleteView(DeleteView):
    model = Label
    template_name = 'labels/label_confirm_delete.html'
    success_url = reverse_lazy('label-list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tasks_with_labels.exists():  # Используем правильное related_name
            messages.error(request, "This label is associated with tasks and cannot be deleted.")
            return render(request, self.template_name, {'object': self.object}, status=200)
        messages.success(request, "Label deleted successfully.")
        return super().post(request, *args, **kwargs)