from django.urls import path
from . import views

urlpatterns = [
    path('signup/artist/', views.artist_signup, name='artist_signup'),
    path('signup/user/', views.user_signup, name='user_signup'),
]
