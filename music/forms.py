from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class ArtistSignUpForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=100,
        required=True,
        help_text=None,  # Remove default help text
    )
    email = forms.EmailField(
        required=True,
        help_text=None,  # Remove default help text
    )
    bank_info = forms.CharField(
        max_length=255,
        required=True,
        help_text=None,  # Remove default help text
    )
    bio = forms.CharField(
        widget=forms.Textarea,
        required=True,
        help_text=None,  # Remove default help text
    )
    certificate_code = forms.CharField(
        max_length=5,
        required=True,
        help_text=None,  # Remove default help text
    )
    genre = forms.CharField(
        max_length=40,
        required=True,
        help_text=None,  # Remove default help text
    )
    profile_picture = forms.ImageField(
        required=False,
        help_text=None,  # Remove default help text
    )

    class Meta:
        model = User
        fields = [
            'username', 'password1', 'password2', 'email', 
            'full_name', 'bank_info', 'bio', 'genre', 
            'certificate_code', 'profile_picture'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help text for all fields
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['email'].help_text = None
        self.fields['full_name'].help_text = None
        self.fields['bank_info'].help_text = None
        self.fields['bio'].help_text = None
        self.fields['certificate_code'].help_text = None
        self.fields['genre'].help_text = None
        self.fields['profile_picture'].help_text = None
        
        # Customize form fields (optional)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['full_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['bank_info'].widget.attrs.update({'class': 'form-control'})
        self.fields['bio'].widget.attrs.update({'class': 'form-control'})
        self.fields['certificate_code'].widget.attrs.update({'class': 'form-control'})
        self.fields['genre'].widget.attrs.update({'class': 'form-control'})
        self.fields['profile_picture'].widget.attrs.update({'class': 'form-control'})


class SimpleUserSignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        help_text=None,  # Remove the default help text
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    # Optionally, you can also set the custom help text or remove it from other fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help text for username and password fields
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        # You can also modify widgets if you want to style fields (optional)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


