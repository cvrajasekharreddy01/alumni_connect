from django.core.management.base import BaseCommand
from django.db import models
from users.models import User
from profiles.models import AlumniProfile

class Command(BaseCommand):
    help = 'Deletes alumni who have not completed their profile (missing full_name or branch)'

    def handle(self, *args, **options):
        # Identify alumni with incomplete profiles
        # We consider a profile incomplete if full_name is empty or branch is empty
        incomplete_alumni = AlumniProfile.objects.filter(
            models.Q(full_name__isnull=True) | models.Q(full_name='') |
            models.Q(branch__isnull=True) | models.Q(branch='')
        )
        
        count = 0
        for profile in incomplete_alumni:
            user = profile.user
            email = user.email
            user.delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted incomplete alumni: {email}'))
            count += 1
            
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} incomplete alumni profiles.'))
