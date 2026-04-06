from django.db import models
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Announcement, AuditLog
from core.forms import AnnouncementForm
from users.models import User, Approval
from mentorship.models import Connection, ResumeReviewRequest, ChatRoom
from profiles.services import MatchingService

from django.utils import timezone

def home(request):
    now = timezone.now()
    announcements = Announcement.objects.filter(
        is_active=True
    ).filter(
        models.Q(expires_at__isnull=True) | models.Q(expires_at__gte=now)
    ).order_by('-created_at')[:5]
    return render(request, 'core/home.html', {'announcements': announcements})

@login_required
def dashboard(request):
    user = request.user
    now = timezone.now()
    announcements = Announcement.objects.filter(
        is_active=True
    ).filter(
        models.Q(expires_at__isnull=True) | models.Q(expires_at__gte=now)
    ).order_by('-created_at')[:5]
    
    context = {
        'announcements': announcements,
    }

    if user.role in ['ADMIN', 'FACULTY']:
        context['announcement_form'] = AnnouncementForm()

    if user.role == 'STUDENT':
        from profiles.models import StudentProfile
        profile, created = StudentProfile.objects.get_or_create(user=user)
        recommendations = MatchingService.get_recommendations(user)
        accepted_connections = Connection.objects.filter(student=user, status='ACCEPTED').select_related('alumni__alumni_profile')
        
        # Add chat room IDs to connections for easy linking
        for conn in accepted_connections:
            room = ChatRoom.objects.filter(student=user, alumni=conn.alumni).first()
            conn.chat_room_id = room.id if room else None

        context.update({
            'recommendations': recommendations,
            'accepted_connections': accepted_connections,
        })
        return render(request, 'core/dashboards/student.html', context)
    
    elif user.role == 'ALUMNI':
        from events.models import Event
        pending_connections = Connection.objects.filter(alumni=user, status='REQUESTED')
        pending_reviews = ResumeReviewRequest.objects.filter(alumni=user, status='PENDING')
        total_mentees = Connection.objects.filter(alumni=user, status='ACCEPTED').count()
        
        events_hosted = Event.objects.filter(created_by=user).count()
        profile_views = user.alumni_profile.views_count
        
        context.update({
            'pending_connections': pending_connections,
            'pending_reviews_count': pending_reviews.count(),
            'total_mentees': total_mentees,
            'events_hosted': events_hosted,
            'profile_views': profile_views,
        })
        return render(request, 'core/dashboards/alumni.html', context)
    
    elif user.role == 'FACULTY':
        return render(request, 'core/dashboards/faculty.html', context)
    
    elif user.role == 'ADMIN':
        from profiles.models import AlumniProfile, CampusPlacement
        from django.db.models import Count
        import json
        
        alumni_qs = AlumniProfile.objects.all()
        placed_count = alumni_qs.filter(campus_placed=True).count()
        not_placed_count = alumni_qs.filter(campus_placed=False).count()
        
        # Company distribution (Top 5)
        company_stats = CampusPlacement.objects.values('company_name').annotate(
            count=Count('company_name')
        ).order_by('-count')[:5]
        
        company_labels = [item['company_name'] for item in company_stats]
        company_counts = [item['count'] for item in company_stats]
        
        alumni_count = User.objects.filter(role='ALUMNI').count()
        student_count = User.objects.filter(role='STUDENT').count()
        faculty_count = User.objects.filter(role='FACULTY').count()
        
        context.update({
            'pending_approvals_count': Approval.objects.filter(status='PENDING').count(),
            'total_alumni_count': alumni_count,
            'total_students_count': student_count,
            'audit_events_count': AuditLog.objects.count(),
            'role_data': [alumni_count, student_count, faculty_count],
            'placement_data': [placed_count, not_placed_count],
            'company_labels': json.dumps(company_labels),
            'company_counts': json.dumps(company_counts),
        })
        return render(request, 'core/dashboards/admin.html', context)
    
    return render(request, 'core/dashboard.html', context)

@login_required
def post_announcement(request):
    if request.user.role not in ['ADMIN', 'FACULTY']:
        messages.error(request, "You don't have permission to post announcements.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            messages.success(request, "Announcement posted successfully!")
            
            # Log the action
            AuditLog.objects.create(
                action_type='POST_ANNOUNCEMENT',
                performed_by=request.user,
                description=f"Posted announcement: {announcement.title}"
            )
            
        else:
            messages.error(request, "Error posting announcement. Please check the form.")
    
    return redirect('dashboard')
