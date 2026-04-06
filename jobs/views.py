from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job
from .forms import JobForm
from users.models import User
from notifications.models import Notification

@login_required
def job_list(request):
    jobs = Job.objects.all().order_by('-created_at')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

@login_required
def post_job(request):
    if request.user.role != 'ALUMNI':
        messages.error(request, "Only alumni can post jobs.")
        return redirect('job-list')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            
            # Notify all students
            students = User.objects.filter(role='STUDENT')
            notification_objs = [
                Notification(
                    user=student,
                    title="New Job Alert!",
                    message=f"A new job '{job.title}' has been posted by {request.user.email} at {job.company}."
                ) for student in students
            ]
            Notification.objects.bulk_create(notification_objs)
            
            messages.success(request, "Job posted successfully and students have been notified!")
            return redirect('job-list')
    else:
        form = JobForm()
    
    return render(request, 'jobs/post_job.html', {'form': form})

@login_required
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'jobs/job_detail.html', {'job': job})
