from django.contrib import messages
from django.db.models import Count, Q, Max, Case, When
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import ArtistSignUpForm, SimpleUserSignUpForm, LoginForm
from .models import User, Artist, Song, LikeHistory, ListeningHistory
from django.utils import timezone

def artist_signup(request):
    if request.method == 'POST':
        form = ArtistSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_artist = True
            user.first_name = form.cleaned_data['full_name']
            user.profile_picture = form.cleaned_data.get('profile_picture')
            user.save()

            Artist.objects.create(
                user=user,
                bio=form.cleaned_data['bio'],
                genre=form.cleaned_data['genre'],
                bank_info=form.cleaned_data['bank_info'],
                certificate_code=form.cleaned_data['certificate_code'],
            )
            login(request, user)
            return redirect('home')
    else:
        form = ArtistSignUpForm()
    return render(request, 'artist_signup.html', {'form': form})

def user_signup(request):
    if request.method == 'POST':
        form = SimpleUserSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.profile_picture = form.cleaned_data.get('profile_picture')
            user.save()
            login(request, user)
            return redirect('home')
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
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def home(request):
    order_by = request.GET.get('order_by')
    liked_filter = request.GET.get('liked')
    search_query = request.GET.get('search', '')
    selected_genre = request.GET.get('genre', '')

    genres = Song.objects.values_list('genre', flat=True).distinct()

    songs = Song.objects.annotate(
        num_likes=Count('likes', distinct=True),
        num_listens=Count('listens', distinct=True),
    )

    if request.user.is_authenticated:
        songs = songs.annotate(
            liked_by_user=Count('likes', filter=Q(likes__user=request.user), distinct=True),
            latest_like_date=Max('likes__liked_at') 
        )
    else:
        songs = songs.annotate(liked_by_user=Count('likes', filter=Q(likes__user=None)))

    if search_query:
        songs = songs.filter(
            Q(title__icontains=search_query) | Q(artist__first_name__icontains=search_query)
        )

    if selected_genre:
        songs = songs.filter(genre=selected_genre)

    if request.user.is_authenticated and liked_filter == 'yes':
        songs = songs.filter(liked_by_user__gt=0).order_by('-latest_like_date')

    if order_by == 'likes_desc':
        songs = songs.order_by('-num_likes')
    elif order_by == 'listens_desc':
        songs = songs.order_by('-num_listens')
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
    song = get_object_or_404(Song, id=song_id)

    if request.user.is_authenticated:
        ListeningHistory.objects.create(song=song, user=request.user, listened_at=timezone.now())

    song.liked_by_user = (
        LikeHistory.objects.filter(song=song, user=request.user).exists()
        if request.user.is_authenticated
        else False
    )

    return render(request, "song_detail.html", {"song": song})

def like_song(request, song_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "You must be logged in to like a song."}, status=403)

    song = get_object_or_404(Song, id=song_id)

    existing_like = LikeHistory.objects.filter(user=request.user, song=song).first()

    if existing_like:
        existing_like.delete()
        liked = False
    else:
        LikeHistory.objects.create(user=request.user, song=song, liked_at=timezone.now())
        liked = True

    return JsonResponse({"liked": liked})

def listening_history(request):
    if not request.user.is_authenticated:
        return redirect('login')

    history = (
        ListeningHistory.objects.filter(user=request.user)
        .values('song_id')
        .annotate(latest_listen_date=Max('listened_at'))
        .order_by('-latest_listen_date')
    )

    song_ids = [item['song_id'] for item in history]
    songs = Song.objects.filter(id__in=song_ids).order_by(
        Case(*[When(id=pk, then=pos) for pos, pk in enumerate(song_ids)])
    )

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


def artist_profile(request, artist_id):
    # Fetch the artist object
    user = get_object_or_404(User, id=artist_id)
    artist = get_object_or_404(Artist, user=user)
    # Fetch all songs by the artist
    songs = Song.objects.filter(artist=user)

    return render(request, 'artist_profile.html', {
        'user': user,
        'songs': songs,
        'artist':artist,
    })


def artist_list(request):
    # Fetch all artists
    artists = User.objects.filter(is_artist=True)
    return render(request, 'artist_list.html', {'artists': artists})
