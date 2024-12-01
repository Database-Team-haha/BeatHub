from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/artist/', views.artist_signup, name='artist_signup'),
    path('signup/user/', views.user_signup, name='user_signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path("songs/<int:song_id>/", views.song_detail, name="song_detail"),
    path("like-song/<int:song_id>/", views.like_song, name="like_song"),
    path('listening-history/', views.listening_history, name='listening_history'),
    path('artists/', views.artist_list, name='artist_list'),
    path('artist/<int:artist_id>/', views.artist_profile, name='artist_profile'),
]
