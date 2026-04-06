from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import User
from profiles.models import StudentProfile, AlumniProfile
from core.models import AuditLog

class Command(BaseCommand):
    help = 'Converts graduated students to alumni based on graduation year'

    def handle(self, *args, **options):
        current_year = timezone.now().year
        graduated_students = StudentProfile.objects.filter(graduation_year__lt=current_year, user__role='STUDENT')
        
        count = 0
        for profile in graduated_students:
            user = profile.user
            old_role = user.role
            user.role = 'ALUMNI'
            user.save()

            # Create AlumniProfile if it doesn't exist
            AlumniProfile.objects.get_or_create(
                user=user,
                defaults={
                    'skills': profile.skills,
                    'industry': 'Unspecified',
                    'company': 'Unspecified',
                    'job_role': 'Graduate Student',
                }
            )

            AuditLog.objects.create(
                action_type='ROLE_CONVERSION',
                performed_by=None,  # System action
                target_user=user,
                description=f"Auto-converted from {old_role} to ALUMNI (Graduation Year: {profile.graduation_year})"
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully converted {count} students to alumni'))
