from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from profil.models import Profil

class EditProfileForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Last Name'}), required=False)
    bio = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Bio'}), required=False)
    url = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'URL'}), required=False)
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Address'}), required=False)

    class Meta:
        model = User
        fields = ['image', 'first_name', 'last_name', 'bio', 'url', 'location']


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': "form-control w-50"
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': "form-control w-50"
    }))
    
    class Meta:
        model = User
        fields = ('email', 'username')
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email',
                'class': "form-control w-50"
            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'Username',
                'class': "form-control w-50"
            }),
        }


    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password1') != cd.get('password2'):
            raise ValidationError("Passwords don't match.")
        return cd['password2']

class LoginForm(forms.Form):
    username = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control w-50' }))
    password = forms.CharField(widget= forms.PasswordInput(attrs={'class': 'form-control w-50'}))