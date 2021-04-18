from django import forms
from .models import Writer
from django.contrib.auth.forms import UserCreationForm

class WriterSignUpForm(UserCreationForm):

    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Enter Username', 'class': 'form-control'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'form-control'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}))
    full_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Enter Full Name', 'class': 'form-control'}))
    bio = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Write About Yourself', 'class': 'form-control'}))

    class Meta:
        model = Writer
        fields = ['username', 'full_name', 'bio', 'image', 'email', 'password1', 'password2']

