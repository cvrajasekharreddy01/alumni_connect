from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Connection, ChatRoom, ChatMessage, ResumeReviewRequest
from users.models import User
from django.contrib import messages
from django.db.models import Q

@login_required
def request_connection(request, alumni_id):
    alumni = get_object_or_404(User, pk=alumni_id, role='ALUMNI')
    Connection.objects.get_or_create(student=request.user, alumni=alumni)
    messages.success(request, f"Connection request sent to {alumni.email}")
    return redirect('alumni-detail', pk=alumni_id)

@login_required
def chat_list(request):
    rooms = ChatRoom.objects.filter(Q(student=request.user) | Q(alumni=request.user))
    return render(request, 'mentorship/chat_list.html', {'rooms': rooms})

@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, pk=room_id)
    if request.user != room.student and request.user != room.alumni:
        return redirect('dashboard')
    
    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            ChatMessage.objects.create(
                room=room,
                sender=request.user,
                message=message_text
            )
            return redirect('chat-room', room_id=room.id)
    
    messages_list = room.messages.all().order_by('timestamp')
    all_rooms = ChatRoom.objects.filter(Q(student=request.user) | Q(alumni=request.user)).order_by('-created_at')
    
    return render(request, 'mentorship/chat_room.html', {
        'room': room, 
        'messages_list': messages_list,
        'all_rooms': all_rooms
    })
@login_required
def accept_connection(request, connection_id):
    connection = get_object_or_404(Connection, pk=connection_id, alumni=request.user)
    connection.status = 'ACCEPTED'
    connection.save()
    
    # Create a chat room automatically
    ChatRoom.objects.get_or_create(student=connection.student, alumni=connection.alumni)
    
    messages.success(request, f"You are now connected with {connection.student.email}")
    return redirect('dashboard')

@login_required
def request_resume_review(request, alumni_id):
    alumni = get_object_or_404(User, pk=alumni_id, role='ALUMNI')
    student_profile = request.user.student_profile
    
    if not student_profile.resume:
        messages.error(request, "Please upload your resume in your profile first.")
        return redirect('edit-profile')
        
    ResumeReviewRequest.objects.get_or_create(
        student=request.user,
        alumni=alumni,
        resume_file=student_profile.resume
    )
    messages.success(request, f"Resume review request sent to {alumni.email}")
    return redirect('alumni-detail', pk=alumni_id)

@login_required
def resume_review_list(request):
    if request.user.role == 'STUDENT':
        reviews = ResumeReviewRequest.objects.filter(student=request.user)
        template = 'mentorship/resume_review_list.html'
    else:
        reviews = ResumeReviewRequest.objects.filter(alumni=request.user)
        template = 'mentorship/resume_review_inbox.html'
        
    if request.method == 'POST' and request.user.role == 'ALUMNI':
        review_id = request.POST.get('review_id')
        feedback = request.POST.get('feedback')
        review = get_object_or_404(ResumeReviewRequest, pk=review_id, alumni=request.user)
        review.feedback = feedback
        review.status = 'REVIEWED'
        review.save()
        messages.success(request, "Feedback submitted successfully!")
        return redirect('resume-review-list')
        
    return render(request, template, {'reviews': reviews})
