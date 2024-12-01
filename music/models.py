from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_artist = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='user_profile/', blank=True, null=True)

class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="artist")
    bio = models.TextField(blank=True)
    genre = models.CharField(max_length=40)
    certificate_code = models.CharField(max_length=5)
    bank_info = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.user.first_name}"
    

class Song(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=40)
    cover_image = models.ImageField(upload_to='cover_images/', blank=True, null=True)
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name="songs")
    file_path = models.FileField(upload_to='songs/')
    upload_date = models.DateField(default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.title} by {self.artist.first_name}"

class ListeningHistory(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="listens")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listened_at = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return f"<{self.song.title}> listened_by {self.user.username}"

class LikeHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="likes")
    liked_at = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return f"<{self.song.title}> liked_by {self.user.username}"

