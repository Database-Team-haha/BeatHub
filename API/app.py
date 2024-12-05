from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Artist, Song, Listening, User, Like
from fastapi.responses import FileResponse
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import joinedload
from fastapi.responses import StreamingResponse
from sqlalchemy import delete
import os
import base64

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/artists/")
async def get_artists(db: Session = Depends(get_db)):
    artists = db.query(Artist).all()
    return artists

@app.post("/artists/")
async def create_artist(username: str, full_name: str, genre: str, bio: str, db: Session = Depends(get_db)):
    artist = Artist(username=username, full_name=full_name, genre=genre, bio=bio)
    db.add(artist)
    db.commit()
    db.refresh(artist)
    return artist


@app.get("/songs/")
async def get_songs(db: Session = Depends(get_db)):
    songs = db.query(Song).options(joinedload(Song.artist)).all()

    for song in songs:
        song.cover_image = os.path.join("http://172.20.10.3:8000/image/", song.cover_image.replace("media/cover_images/", ""))
        
        image = song.artist.profile_picture.replace("media/user_profile/", "")
        image =  image.replace(" ", "_")
        song.artist_picture = "http://172.20.10.3:8000/picture/" + image


    return songs

@app.get("/image/{image_filename}")
async def get_image(image_filename: str):
    image_path = os.path.join("media/cover_images/", image_filename)
    
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        return {"error": "Image not found"}

@app.get("/picture/{image_filename}")
async def get_image(image_filename: str):
    image_path = os.path.join("media/user_profile/", image_filename)
    
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        return {"error": "Image not found"}


@app.post("/songs/")
async def create_song(title: str, genre: str, artist_username: str, song_path: str, db: Session = Depends(get_db)):
    song = Song(title=title, genre=genre, artist_username=artist_username, song_path=song_path)
    db.add(song)
    db.commit()
    db.refresh(song)
    return song


@app.get("/listenings/")
async def get_listenings(username: str, db: Session = Depends(get_db)):
    if not username:
        raise HTTPException(status_code=400, detail="Username is required")

    listenings = db.query(Listening).filter(Listening.user_username == username).all()

    if not listenings:
        raise HTTPException(status_code=404, detail="No listenings found for this user")
    
    if listenings[len(listenings)-1].song.cover_image:
        image = listenings[len(listenings)-1].song.cover_image.replace("media/cover_images/", "")
        image =  "http://172.20.10.3:8000/image/" + image

    return {
        "song_id": listenings[len(listenings)-1].song_id,
        "title":listenings[len(listenings)-1].song.title,
        "artist_username":listenings[len(listenings)-1].song.artist_username,
        "cover_image":image,
    }
    

@app.post("/listenings/")
async def create_listening(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    song_id = data.get("song_id")
    user_username = data.get("username")
    listening = Listening(song_id=song_id, user_username=user_username, listened_at=datetime.now())
    db.add(listening)
    db.commit()
    db.refresh(listening)
    return listening

@app.post("/users/login/")
async def login(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    username = data.get("user_username")
    password = data.get("password")

    print(f'Username: {username}, password: {password}')

    user = db.query(User).filter(User.username == username).first()
    print(f"User: {user.password}")
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if user.profile_picture:
        image = user.profile_picture.replace("media/user_profile/", "")
        image =  "http://172.20.10.3:8000/picture/" + image

    return {
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "date_joined": user.date_joined,
        "profile_picture": image,
    }



@app.get("/users/")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.post("/users/")
async def create_user(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    fullname = data.get("fullname")
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    user = User(username=username, full_name=fullname, password=password, email=email, date_joined=datetime.now())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/songs/{song_id}/stream/")
async def stream_song(song_id: int, db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song or not os.path.exists(song.song_path):
        raise HTTPException(status_code=404, detail=f"Song not found {song.song_path}")

    file = open(song.song_path, "rb")
    return StreamingResponse(file, media_type="audio/mp3")

@app.post("/songs/{song_id}/like/")
async def like_song(request: Request, song_id: int, db: Session = Depends(get_db)):
    data = await request.json()
    username = data.get("username")

    
    existing_like = db.query(Like).filter(Like.song_id == song_id, Like.user_username == username).first()
    
    if existing_like:
        raise HTTPException(status_code=400, detail="Song already liked")
    
    new_like = Like(
        song_id=song_id, 
        user_username=username, 
        liked_at=datetime.now()
    )
    db.add(new_like)
    db.commit()
    
    return {"message": "Song liked successfully"}

@app.post("/songs/{song_id}/dislike/")
async def dislike_song(request: Request, song_id: int, db: Session = Depends(get_db)):
    data = await request.json()
    username = data.get("username")
    
    existing_like = db.query(Like).filter(Like.song_id == song_id, Like.user_username == username).first()
    
    if not existing_like:
        raise HTTPException(status_code=400, detail="Song not liked")
    
    db.delete(existing_like)
    db.commit()
    
    return {"message": "Song disliked successfully"}


@app.get("/users/{username}/liked_songs/")
async def get_liked_songs(username: str, db: Session = Depends(get_db)):
    liked_songs = (
        db.query(Song)
        .join(Like, Song.id == Like.song_id)
        .filter(Like.user_username == username)
        .all()
    )

    if not liked_songs:
        raise HTTPException(status_code=404, detail="No liked songs found for this user")

    for song in liked_songs:
        song.cover_image = os.path.join(
            "http://172.20.10.3:8000/image/", 
            song.cover_image.replace("media/cover_images/", "")
        )
        
        image = song.artist.profile_picture.replace("media/user_profile/", "")
        image = image.replace(" ", "_")
        song.artist_picture = "http://172.20.10.3:8000/picture/" + image

    return liked_songs

