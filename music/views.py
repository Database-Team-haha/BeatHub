
from django.contrib import messages
from django.db.models import Count, Q, Max, Case, When
# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import ArtistSignUpForm, SimpleUserSignUpForm, LoginForm
from .models import User, Artist, Song, LikeHistory, ListeningHistory
from django.utils import timezone

def artist_signup(request):
    if request.method == 'POST':
        form = ArtistSignUpForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            user = form.save(commit=False)
            user.is_artist = True  # Mark as artist
            user.first_name = form.cleaned_data['full_name']
            user.profile_picture = form.cleaned_data.get('profile_picture')  # Correctly save the profile_picture
            user.save()
        
            artist = Artist.objects.create(
                user=user,
                bio=form.cleaned_data['bio'],
                genre=form.cleaned_data['genre'],
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


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a homepage or dashboard
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            print(form.errors)
            messages.error(request, 'Invalid form submission.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'home.html')



def home(request):
    # Get the query parameters for sorting, searching, and genre
    order_by = request.GET.get('order_by')
    liked_filter = request.GET.get('liked')
    search_query = request.GET.get('search', '')
    selected_genre = request.GET.get('genre', '')

    # Get all unique genres from the Song model
    genres = Song.objects.values_list('genre', flat=True).distinct()

    # Annotate songs with the number of likes and listens
    songs = Song.objects.annotate(
        num_likes=Count('likes', distinct=True),
        num_listens=Count('listens', distinct=True),
        liked_by_user=Count('likes', filter=Q(likes__user=request.user), distinct=True)
    )

    # Filter songs by search query (title or artist name)
    if search_query:
        songs = songs.filter(
            Q(title__icontains=search_query) | Q(artist__first_name__icontains=search_query)
        )

    # Filter by genre if a genre is selected
    if selected_genre:
        songs = songs.filter(genre=selected_genre)

    # If the user is logged in and the liked filter is applied
    if request.user.is_authenticated and liked_filter == 'yes':
        songs = songs.filter(liked_by_user__gt=0)

    # Sort the songs based on the selected filter
    if order_by == 'likes_desc':
        songs = songs.order_by('-num_likes')  # Sort by likes DESC
    elif order_by == 'listens_desc':
        songs = songs.order_by('-num_listens')  # Sort by listens DESC
    elif order_by == 'recency':
        songs = songs.order_by('-upload_date')

    return render(request, 'home.html', {
        'songs': songs,
        'order_by': order_by,
        'search_query': search_query,
        'genres': genres,
        'selected_genre': selected_genre
    })


def song_detail(request, song_id):
    # Fetch the song
    song = get_object_or_404(Song, id=song_id)

    # Add to listening history if the user is logged in
    if request.user.is_authenticated:
        ListeningHistory.objects.create(song=song, user=request.user, listened_at=timezone.now())

    # Annotate the song with the like information for the current user
    if request.user.is_authenticated:
        song.liked_by_user = LikeHistory.objects.filter(song=song, user=request.user).exists()
    else:
        song.liked_by_user = False

    # Render the song detail template
    return render(request, "song_detail.html", {"song": song})


def like_song(request, song_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "You must be logged in to like a song."}, status=403)

    song = get_object_or_404(Song, id=song_id)

    # Check if the user has already liked this song
    existing_like = LikeHistory.objects.filter(user=request.user, song=song).first()

    if existing_like:
        # If liked, remove the like
        existing_like.delete()
        liked = False
    else:
        # If not liked, create a new like
        LikeHistory.objects.create(user=request.user, song=song, liked_at=timezone.now())
        liked = True

    return JsonResponse({"liked": liked})


from django.db.models import Max

def listening_history(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if the user is not authenticated

    # Fetch unique songs the user has listened to and their latest listening date
    history = (
        ListeningHistory.objects.filter(user=request.user)
        .values('song_id')
        .annotate(latest_listen_date=Max('listened_at'))
        .order_by('-latest_listen_date')  # Order by latest listening date in descending order
    )

    # Fetch related song objects in the same order as `history`
    song_ids = [item['song_id'] for item in history]
    songs = Song.objects.filter(id__in=song_ids).order_by(
        # Preserve the order of song_ids (same as in history)
        Case(*[When(id=pk, then=pos) for pos, pk in enumerate(song_ids)])
    )

    # Combine song details with listening date
    listening_data = [
        {
            'song': song,
            'listened_date': next(
                (item['latest_listen_date'] for item in history if item['song_id'] == song.id), None
            )
        }
        for song in songs
    ]

    return render(request, 'listening_history.html', {'listening_data': listening_data})



