from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class ArtistSignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    bank_info = forms.CharField(max_length=255, required=True)
    bio = forms.CharField(widget=forms.Textarea, required=True)
    certificate_code = forms.CharField(max_length=5, required=True)
    genre = forms.CharField(max_length=40, required=True)
    profile_picture = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'full_name', 'bank_info', 'bio', 'genre', 'certificate_code', 'profile_picture']

class SimpleUserSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


