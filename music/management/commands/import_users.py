import pandas as pd
from django.core.management.base import BaseCommand
from music.models import User
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_datetime
from django.core.files import File

class Command(BaseCommand):
    help = 'Import users from an Excel file into the User model'

    def add_arguments(self, parser):
        # Allow the user to specify the Excel file as an argument
        parser.add_argument('file', type=str)

    def handle(self, *args, **kwargs):
        file_path = kwargs['file']
        try:
            # Read the Excel file into a pandas DataFrame
            df = pd.read_excel(file_path)

            # Iterate over the rows and save each user
            for index, row in df.iterrows():
                try:
                    # Prepare the data for the user
                    username = row['username']
                    password = row['password']
                    profile_picture = row['profile_picture'] or None
                    date_joined = parse_datetime(row['date_joined'])

                    # Create the user instance
                    user = User(
                        username=username,
                        email=row.get('email', ''),  # Optional email
                        date_joined=date_joined,
                    )

                    # Set the password (Django requires hashing the password)
                    user.set_password(password)

                    # Handle the cover image upload if it exists
                    if pd.notna(profile_picture):  # Check if there's a cover image
                        with open(profile_picture, 'rb') as f:
                            user.profile_picture.save(profile_picture.split('/')[-1], File(f), save=True)

                    # Save the user to the database
                    user.save()

                    self.stdout.write(self.style.SUCCESS(f'Successfully added user: {username}'))

                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f'Error adding user at row {index}: {e}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Unexpected error at row {index}: {e}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading the Excel file: {e}'))

