from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
GENRE_CHOICES = [
    ('pop', 'Pop'),
    ('classical', 'Classical')
]

class User(AbstractUser):
    is_artist = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='user_profile/', blank=True, null=True)

class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="artist")
    bio = models.TextField(blank=True)
    genre = models.CharField(max_length=40, choices=GENRE_CHOICES, default='pop')
    certificate_code = models.CharField(max_length=5)
    bank_info = models.CharField(max_length=16)

class Song(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=40, choices=GENRE_CHOICES, default='pop')
    cover_image = models.ImageField(upload_to='cover_images/', blank=True, null=True)
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name="songs")
    file_path = models.FileField(upload_to='songs/')
    upload_date = models.DateField(auto_now_add=True)

class ListeningHistory(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="listens")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listens")
    listened_at = models.DateTimeField(auto_now_add=True)

class LikeHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="likes")
    liked_at = models.DateTimeField(auto_now_add=True)



    


