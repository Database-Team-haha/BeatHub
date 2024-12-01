import pandas as pd
from django.core.management.base import BaseCommand
from music.models import Song, User
from django.core.exceptions import ValidationError
from django.core.files import File
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Import songs from an Excel file into the Song model'

    def add_arguments(self, parser):
        # Allow the user to specify the Excel file as an argument
        parser.add_argument('file', type=str)

    def handle(self, *args, **kwargs):
        file_path = kwargs['file']

        try:
            # Read the Excel file into a pandas DataFrame
            df = pd.read_excel(file_path)

            # Iterate over the rows and save each song
            for index, row in df.iterrows():
                try:
                    # Prepare the data for the song
                    title = row['title']
                    artist_username = row['artist_username']  # The username of the artist
                    genre = row['genre']
                    cover_image = row['cover_image'] or None
                    release_date = row['upload_date']
                    song_file = row['song_path'] or None

                    # Look up the artist by username
                    artist = User.objects.get(username=artist_username)
                    
                    # Create the song instance
                    song = Song(
                        id = index+1,
                        title=title,
                        artist=artist,
                        genre=genre,
                        upload_date=release_date,
                    )
                    if pd.notna(cover_image):  # Check if there's a cover image
                        with open(cover_image, 'rb') as f:
                            song.cover_image.save(cover_image.split('/')[-1], File(f), save=True)
                    # Handle the song file upload if it exists
                    if pd.notna(song_file):  # Check if there's a song file
                        song_file_path = os.path.join(settings.BASE_DIR, song_file)
                        if os.path.exists(song_file_path):
                            with open(song_file_path, 'rb') as f:
                                song.file_path.save(song_file.split('/')[-1], File(f), save=True)
                        else:
                            self.stdout.write(self.style.ERROR(f'File not found: {song_file}'))

                    # Save the song to the database
                    song.save()

                    self.stdout.write(self.style.SUCCESS(f'Successfully added song: {title}'))

                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f'Error adding song at row {index}: {e}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Unexpected error at row {index}: {e}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading the Excel file: {e}'))
