# users/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=150,
        required=True,
    )
    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=150,
        required=True,
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
