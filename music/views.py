from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import ArtistSignUpForm, SimpleUserSignUpForm
from .models import User, Artist

def artist_signup(request):
    if request.method == 'POST':
        form = ArtistSignUpForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            user = form.save(commit=False)
            user.is_artist = True  # Mark as artist
            user.profile_picture = form.cleaned_data.get('profile_picture')  # Correctly save the profile_picture
            user.save()
        
            artist = Artist.objects.create(
                user=user,
                bio=form.cleaned_data['bio'],
                bank_info=form.cleaned_data['bank_info'],
                certificate_code=form.cleaned_data['certificate_code'],
            )
            artist.save()
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to the homepage or artist dashboard
    else:
        form = ArtistSignUpForm()
    return render(request, 'artist_signup.html', {'form': form})

def user_signup(request):
    if request.method == 'POST':
        form = SimpleUserSignUpForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            user = form.save(commit=False)
            user.profile_picture = form.cleaned_data.get('profile_picture')  # Correctly save the profile_picture
            user.save()
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to the homepage or user dashboard
    else:
        form = SimpleUserSignUpForm()
    return render(request, 'user_signup.html', {'form': form})
