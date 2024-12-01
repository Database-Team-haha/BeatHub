from django.contrib import admin
from music.models import User, Artist, Song, ListeningHistory, LikeHistory
# Register your models here.
admin.site.register(User)
admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(ListeningHistory)
admin.site.register(LikeHistory)