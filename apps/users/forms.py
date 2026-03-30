from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import ContactUs, User


INPUT_CLASS = (
    'w-full rounded-2xl border border-slate-200 bg-white/90 px-4 py-3 text-sm '
    'text-slate-800 shadow-sm outline-none transition focus:border-sky-500 focus:ring-4 focus:ring-sky-100'
)
TEXTAREA_CLASS = (
    'w-full rounded-2xl border border-slate-200 bg-white/90 px-4 py-3 text-sm '
    'text-slate-800 shadow-sm outline-none transition focus:border-sky-500 focus:ring-4 focus:ring-sky-100 min-h-[180px]'
)


# forms for user signup and login views that create users and authenticate users in the database
class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Ism'}),
            'last_name': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Familiya'}),
            'username': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Email'}),
        }

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Parol'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Parolni tasdiqlang'}))


class UserSigninForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Parol'}))


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'image', 'phone_number', 'email', 'username']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Ism'}),
            'last_name': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Familiya'}),
            'image': forms.FileInput(attrs={'class': INPUT_CLASS}),
            'phone_number': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '+998901234567'}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Email', 'readonly': True}),
            'username': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Username', 'readonly': True}),
        }


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['full_name', 'email', 'phone_number', 'message']

        widgets = {
            'full_name': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Ism va familiya'}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Email manzil'}),
            'phone_number': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '+998901234567'}),
            'message': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'placeholder': 'Maqsadingiz, qiziqayotgan kurs yoki savolingizni yozing'}),
        }
