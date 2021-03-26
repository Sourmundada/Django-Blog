from django import forms
from .models import Post, Comment
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from ckeditor.widgets import CKEditorWidget
from taggit.forms import TagField, TagWidget
from django.contrib.auth.models import User
from django.contrib.admin.forms import PasswordChangeForm

class PostForm(forms.ModelForm):

    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    slug = forms.SlugField(label='', widget=forms.TextInput(attrs={'placeholder': 'enter-slug-here'}))
    # category = forms.CharField(label='', widget=forms.MultipleChoiceField())
    thumbnail = forms.ImageField(label='Thumbnail', required=False)
    content = forms.CharField(label='', widget=CKEditorWidget(attrs={'placeholder': 'Your Content'}))
    # status = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Choose Status'}))
    tags = TagField(label='', widget=TagWidget(attrs={'placeholder': 'tags, tags, tags'}))


    class Meta:
        model = Post
        fields = ['title', 'slug', 'category', 'author', 'thumbnail', 'content', 'status', 'tags']

class CommentForm(forms.ModelForm):

    name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Enter Your Name', 'class': 'form-control'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Enter Your Email', 'class': 'form-control'}))
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Your Comment', 'rows': 3, 'class': 'form-control'}))

    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']


class SignUpForm(UserCreationForm):

    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Enter Username', 'class': 'form-control'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'form-control'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):

    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Your Username', 'class': 'form-control'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password']

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Old Password', 'class': 'form-control'}))
    new_password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'New Password', 'class': 'form-control'}))
    new_password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password', 'class': 'form-control'}))
