from django.core.management.base import BaseCommand
from users.models import User, Approval
from profiles.models import StudentProfile, AlumniProfile, PlacementDetails
from core.models import Announcement
from events.models import Event
from django.utils import timezone
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Generates sample data for testing'

    def handle(self, *args, **options):
        # Create Admin
        admin, _ = User.objects.get_or_create(
            email='admin@college.edu',
            defaults={
                'role': 'ADMIN',
                'is_approved': True,
                'is_staff': True,
                'is_superuser': True,
                'password': make_password('admin123')
            }
        )

        # Create Alumni
        alumni_user, _ = User.objects.get_or_create(
            email='alumni@google.com',
            defaults={
                'role': 'ALUMNI',
                'is_approved': True,
                'password': make_password('alumni123')
            }
        )
        alumni_profile, _ = AlumniProfile.objects.get_or_create(
            user=alumni_user,
            defaults={
                'company': 'Google',
                'job_role': 'Software Engineer',
                'industry': 'Technology',
                'experience_years': 5,
                'skills': ['Python', 'Django', 'React'],
                'is_verified': True
            }
        )
        PlacementDetails.objects.get_or_create(
            alumni=alumni_profile,
            company='Google',
            role='SDE-2',
            year=2021
        )

        # Create Student
        student_user, _ = User.objects.get_or_create(
            email='student@college.edu',
            defaults={
                'role': 'STUDENT',
                'is_approved': True,
                'password': make_password('student123')
            }
        )
        StudentProfile.objects.get_or_create(
            user=student_user,
            defaults={
                'department': 'Computer Science',
                'graduation_year': 2026,
                'skills': ['Python', 'Django'],
                'career_interest': 'Technology'
            }
        )

        # Announcements
        Announcement.objects.get_or_create(
            title='Welcome to Alumni Connect!',
            message='We are excited to launch our new portal for students and alumni.',
            created_by=admin
        )

        # Events
        Event.objects.get_or_create(
            title='Career in Big Tech',
            description='A workshop on how to crack interviews at FAANG companies.',
            speaker=alumni_user,
            event_date=timezone.now() + timezone.timedelta(days=7),
            event_type='WORKSHOP',
            created_by=admin
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded sample data'))
