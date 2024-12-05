import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, TIMESTAMP, ForeignKey

load_dotenv(dotenv_path=".env")

# Database configuration
DATABASE_URL = f"postgresql://{os.getenv('USER_DB')}:{os.getenv('PASSWORD_DB')}@{os.getenv('HOST_DB')}:{os.getenv('PORT_DB')}/{os.getenv('NAME_DB')}"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define tables
artists = Table(
    "artists",
    metadata,
    Column("username", String, primary_key=True),
    Column("full_name", String),
    Column("password", String),
    Column("email", String),
    Column("date_joined", Date),
    Column("profile_picture", String),
    Column("bio", String),
    Column("genre", String),
    Column("certification_code", String),
    Column("bank_info", String),
)

songs = Table(
    "songs",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String),
    Column("genre", String),
    Column("cover_image", String),
    Column("artist_username", String, ForeignKey("artists.username")),
    Column("song_path", String),
    Column("upload_date", Date),
)

users = Table(
    "users",
    metadata,
    Column("username", String, primary_key=True),
    Column("full_name", String),
    Column("password", String),
    Column("email", String),
    Column("date_joined", Date),
    Column("profile_picture", String),
)

listenings = Table(
    "listenings",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("song_id", Integer, ForeignKey("songs.id")),
    Column("user_username", String),
    Column("listened_at", TIMESTAMP),
)

likes = Table(
    "likes",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("song_id", Integer, ForeignKey("songs.id")),
    Column("user_username", String),
    Column("liked_at", Date),
)

# Create tables
metadata.create_all(engine)

# Load data from Excel files
file_table_mapping = {
    "../datas/artists.xlsx": artists,
    "../datas/songs.xlsx": songs,
    "../datas/users.xlsx": users,
    "../datas/listenings.xlsx": listenings,
    "../datas/likes.xlsx": likes,
}

# Insert the artists and users data into their respective tables
for file, table in file_table_mapping.items():
    print(f"Loading {file} into {table.name}...")
    df = pd.read_excel(file)  # Read the Excel file into a DataFrame
    df.to_sql(table.name, con=engine, if_exists="append", index=False)
    print(f"Finished loading {file} into {table.name}.")
