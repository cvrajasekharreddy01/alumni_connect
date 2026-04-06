from django.db import models
from django.conf import settings

class Job(models.Model):
    job_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    apply_link = models.URLField(max_length=500, null=True, blank=True, help_text="Link to apply for the job")
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobs_posted')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company} ({self.job_id})"
