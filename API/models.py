from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Artist(Base):
    __tablename__ = "artists"

    username = Column(String, primary_key=True)
    full_name = Column(String)
    password = Column(String)
    email = Column(String)
    date_joined = Column(Date)
    profile_picture = Column(String)
    bio = Column(String)
    genre = Column(String)
    certification_code = Column(String)
    bank_info = Column(String)

    # Relationship with Song
    songs = relationship("Song", back_populates="artist")

class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    genre = Column(String)
    cover_image = Column(String)
    artist_username = Column(String, ForeignKey("artists.username"))
    song_path = Column(String)
    upload_date = Column(Date)

    # Relationship with Artist
    artist = relationship("Artist", back_populates="songs")

    # Relationship with Listening
    listenings = relationship("Listening", back_populates="song")

    # Relationship with Like (added)
    likes = relationship("Like", back_populates="song")

class Listening(Base):
    __tablename__ = "listenings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    song_id = Column(Integer, ForeignKey("songs.id"))
    user_username = Column(String, ForeignKey("users.username"))
    listened_at = Column(TIMESTAMP)

    # Relationships with Song and User
    song = relationship("Song", back_populates="listenings")
    user = relationship("User", back_populates="listenings")

class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True)
    full_name = Column(String)
    password = Column(String)
    email = Column(String)
    date_joined = Column(Date)
    profile_picture = Column(String)

    # Relationship with Listening
    listenings = relationship("Listening", back_populates="user")

    # Relationship with Like (added)
    likes = relationship("Like", back_populates="user")

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    song_id = Column(Integer, ForeignKey("songs.id"))
    user_username = Column(String, ForeignKey("users.username"))
    liked_at = Column(Date)

    # Relationships
    song = relationship("Song", back_populates="likes")
    user = relationship("User", back_populates="likes")
