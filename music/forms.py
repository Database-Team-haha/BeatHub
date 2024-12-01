from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, GENRE_CHOICES

class ArtistSignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    bank_info = forms.CharField(max_length=255, required=True)
    bio = forms.CharField(widget=forms.Textarea, required=True)
    certificate_code = forms.CharField(max_length=5, required=True)
    genre = forms.ChoiceField(choices=GENRE_CHOICES, required=True)
    profile_picture = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'full_name', 'bank_info', 'bio', 'genre', 'certificate_code', 'profile_picture']

class SimpleUserSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
