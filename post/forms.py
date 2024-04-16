from django import forms
from post.models import Post


from django import forms
from post.models import Post

class NewPostform(forms.ModelForm):
    picture = forms.FileField(
        required=True, 
        widget=forms.FileInput(attrs={
            'accept': 'image/*,video/*',
            'class': 'form-control'
        })
    )
    caption = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Caption'
        }), 
        required=True
    )
    tags = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tags | Separate with comma'
        }), 
        required=True
    )

    class Meta:
        model = Post
        fields = ['picture', 'caption', 'tags']


