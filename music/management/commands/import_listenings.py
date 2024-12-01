import pandas as pd
from django.core.management.base import BaseCommand
from music.models import ListeningHistory, Song, User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateparse import parse_date

class Command(BaseCommand):
    help = 'Import likes data from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **kwargs):
        file_path = kwargs['file']

        try:
            # Read the Excel file into a pandas DataFrame
            df = pd.read_excel(file_path)

            # Iterate over the rows and save each like
            for index, row in df.iterrows():
                try:
                    # Extract and validate data from row
                    song_id = row['song_id']
                    username = row['user_username']
                    listened_at_str = row['listened_at']

                    # Parse liked_at to a valid date object
                    listened_at = parse_date(str(listened_at_str))
                    if not listened_at:
                        raise ValueError(f"Invalid date format at row {index}")

                    # Fetch the Song and User instances
                    song = Song.objects.get(id=song_id)
                    user = User.objects.get(username=username)

                    # Create the LikeHistory instance
                    listening = ListeningHistory(
                        id = index+1,
                        song=song, 
                        user=user, 
                        listened_at=listened_at
                    )
                    listening.save()
                    self.stdout.write(self.style.SUCCESS(f"Successfully added like: {user.username} -> {song.title}"))
                    

                except ObjectDoesNotExist as e:
                    self.stdout.write(self.style.ERROR(f"Error at row {index}: {e}"))
                except ValueError as e:
                    self.stdout.write(self.style.ERROR(f"Error at row {index}: {e}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Unexpected error at row {index}: {e}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading the Excel file: {e}"))
