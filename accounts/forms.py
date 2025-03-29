from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email address')}),
        required=True
    )
    
    first_name_en = forms.CharField(
        label=_("First Name (English)"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('First name in English')}),
        required=True
    )
    
    last_name_en = forms.CharField(
        label=_("Last Name (English)"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Last name in English')}),
        required=True
    )
    
    first_name_ar = forms.CharField(
        label=_("First Name (Arabic)"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('First name in Arabic')}),
        required=False
    )
    
    last_name_ar = forms.CharField(
        label=_("Last Name (Arabic)"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Last name in Arabic')}),
        required=False
    )

    class Meta:
        model = User
        fields = ['first_name_en', 'last_name_en', 'first_name_ar', 'last_name_ar', 'email', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'password1': _('Password'),
            'password2': _('Password Confirmation'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email address')})
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Password')})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages['invalid_login'] = _(
            "Please enter a correct email and password. Note that both fields may be case-sensitive."
        )