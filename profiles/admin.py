from django.contrib import admin
from .models import StudentProfile, AlumniProfile, PlacementDetails

admin.site.register(StudentProfile)
admin.site.register(AlumniProfile)
admin.site.register(PlacementDetails)
