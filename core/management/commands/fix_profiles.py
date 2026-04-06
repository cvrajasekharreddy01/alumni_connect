from django.core.management.base import BaseCommand
from users.models import User
from profiles.models import StudentProfile, AlumniProfile

class Command(BaseCommand):
    help = 'Creates profiles for users who do not have them'

    def handle(self, *args, **options):
        # Fix Students
        students = User.objects.filter(role='STUDENT')
        student_count = 0
        for student in students:
            profile, created = StudentProfile.objects.get_or_create(user=student)
            if created:
                student_count += 1
        
        # Fix Alumni
        alumni = User.objects.filter(role='ALUMNI')
        alumni_count = 0
        for alum in alumni:
            profile, created = AlumniProfile.objects.get_or_create(user=alum)
            if created:
                alumni_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {student_count} student profiles and {alumni_count} alumni profiles.'))
