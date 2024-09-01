from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')


class UserUpdateView(UpdateView):
    model = User
    template_name = 'users/user_form.html'
    fields = ['username', 'first_name', 'last_name', 'email']
    success_url = reverse_lazy('user-list')


class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user-list')


class LoginView(auth_views.LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('home')