from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class CustomUserForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control modern-input',
            'placeholder': 'Enter Username'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control modern-input',
            'placeholder': 'Enter Email Address'
        })
    )

    mobile = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control modern-input',
            'placeholder': 'Enter Mobile Number'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control modern-input',
            'placeholder': 'Enter Password'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control modern-input',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'mobile', 'password1', 'password2']