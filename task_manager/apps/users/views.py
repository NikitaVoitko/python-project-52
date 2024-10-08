from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CustomAuthenticationForm, UserCreationForm, UserUpdateForm
from .models import User
from task_manager.apps.tasks.models import Task
from django.contrib.messages.views import SuccessMessageMixin


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')
    success_message = "Пользователь успешно зарегистрирован"


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('user-list')

    def form_valid(self, form):
        if form.cleaned_data.get('password1'):
            self.object.set_password(form.cleaned_data['password1'])
        self.object.save()
        messages.success(self.request, "Пользователь успешно изменен")
        return super().form_valid(form)

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для изменения другого пользователя.")
        return redirect('user-list')


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user-list')

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для изменения")
        return redirect('user-list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_in_use = (
            Task.objects.filter(executor=self.object).exists()
            or Task.objects.filter(author=self.object).exists()
        )
        if user_in_use:
            messages.error(
                self.request,
                "Невозможно удалить пользователя, потому что он используется"
            )
            return redirect(self.success_url)

        messages.success(self.request, "Пользователь успешно удален")
        return super().post(request, *args, **kwargs)


class LoginView(auth_views.LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, 'Вы залогинены')
        return super().form_valid(form)


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Вы разлогинены')
        return super().dispatch(request, *args, **kwargs)
