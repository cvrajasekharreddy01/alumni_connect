from django.contrib import admin
from .models import Announcement, AuditLog

admin.site.register(Announcement)
admin.site.register(AuditLog)
