from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, ContactUs


# forms for user signup and login views that create users and authenticate users in the database
class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        }


class UserSigninForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'image', 'phone_number', 'email', 'username']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Enter image'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email', 'readonly': True}),
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter username', 'readonly': True}),
        }


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['full_name', 'email', 'phone_number', 'message']

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'col-lg-6', 'placeholder': 'Enter full name'}),
            'email': forms.EmailInput(attrs={'class': 'col-lg-6', 'placeholder': 'Enter email'}),
            'phone_number': forms.TextInput(attrs={'class': 'col-lg-6', 'placeholder': 'Enter phone number'}),
            'message': forms.Textarea(attrs={'class': 'col-lg-6', 'placeholder': 'Enter message'}),
        }