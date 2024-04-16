from django import forms
from django.contrib.auth.models import User

from .models import Profil

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']



class ProfilUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    
    class Meta:
        model = Profil
        fields = ['username', 'fullname', 'birthday', 'gender', 'public']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfilUpdateForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:  # Make sure there's a related user instance
            self.fields['username'].initial = self.instance.user.username

    def save(self, commit=True):
        profil = super().save(commit=False)
        if 'username' in self.cleaned_data:
            profil.user.username = self.cleaned_data['username']
            profil.user.save()
        if commit:
            profil.save()
        return profil