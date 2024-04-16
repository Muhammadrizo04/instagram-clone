from django.db import models
from django.contrib.auth.models import User
import PIL 
from PIL import Image
from post.models import Post
from django.core.exceptions import ValidationError


class Profil(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    username = models.CharField(max_length=20)
    email = models.EmailField()
    bio = models.CharField(max_length=155, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    image = models.ImageField(upload_to="profile_pciture", null=True, default="default.jpg")
    fullname = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='followings', through='Relationship')
    public = models.BooleanField(default=True)
    favourite = models.ManyToManyField(Post, blank=True)
    url = models.URLField(max_length=200, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} - Profil'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        

class Relationship(models.Model):
    follower = models.ForeignKey(Profil, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(Profil, related_name='following', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    