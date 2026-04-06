from django.db import models
from django.conf import settings

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    full_name = models.CharField(max_length=200, null=True, blank=True)
    roll_number = models.CharField(max_length=50, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    branch = models.CharField(max_length=100, null=True, blank=True)
    skills = models.JSONField(default=list)
    interests = models.TextField(blank=True)
    career_interest = models.CharField(max_length=200, null=True, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    bio = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    def __str__(self):
        return f"Student: {self.user.email}"

class AlumniProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alumni_profile')
    full_name = models.CharField(max_length=200, null=True, blank=True)
    roll_number = models.CharField(max_length=50, null=True, blank=True)
    branch = models.CharField(max_length=100, null=True, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    campus_placed = models.BooleanField(default=False)
    
    # Keeping old fields for compatibility during transition if needed, but primarily using the new ones
    company = models.CharField(max_length=200, null=True, blank=True)
    job_role = models.CharField(max_length=100, null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    skills = models.JSONField(default=list)
    bio = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Alumni: {self.user.email} ({self.full_name or 'No Name'})"

class CampusPlacement(models.Model):
    alumni = models.OneToOneField(AlumniProfile, on_delete=models.CASCADE, related_name='campus_placement')
    company_name = models.CharField(max_length=200, null=True, blank=True)
    job_role = models.CharField(max_length=100, null=True, blank=True)
    ctc = models.CharField(max_length=50, null=True, blank=True)
    placement_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Campus Placement: {self.alumni.user.email} at {self.company_name or 'N/A'}"

class Experience(models.Model):
    alumni = models.ForeignKey(AlumniProfile, on_delete=models.CASCADE, related_name='experiences')
    company_name = models.CharField(max_length=200, null=True, blank=True)
    job_role = models.CharField(max_length=100, null=True, blank=True)
    ctc = models.CharField(max_length=50, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    experience_description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.job_role} at {self.company_name} ({self.alumni.user.email})"

class PlacementDetails(models.Model):
    alumni = models.ForeignKey(AlumniProfile, on_delete=models.CASCADE, related_name='placements')
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=100)
    year = models.IntegerField()
    status = models.CharField(max_length=20, choices=[('PLACED', 'Placed'), ('NOT_PLACED', 'Not Placed')], default='PLACED')

    def __str__(self):
        return f"{self.alumni.user.email} at {self.company}"
