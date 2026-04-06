from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Approval
from profiles.models import StudentProfile, AlumniProfile

@receiver(post_save, sender=User)
def create_user_related_objects(sender, instance, created, **kwargs):
    if created:
        # Create Approval record
        Approval.objects.get_or_create(user=instance)
        
        # Create Profile based on role
        if instance.role == 'STUDENT':
            StudentProfile.objects.get_or_create(user=instance)
        elif instance.role == 'ALUMNI':
            AlumniProfile.objects.get_or_create(user=instance)
