from django.urls import path
from . import views

urlpatterns = [
    path('request/<int:alumni_id>/', views.request_connection, name='request-connection'),
    path('chats/', views.chat_list, name='chat-list'),
    path('chat/<int:room_id>/', views.chat_room, name='chat-room'),
    path('accept/<int:connection_id>/', views.accept_connection, name='accept-connection'),
    path('resume-review/request/<int:alumni_id>/', views.request_resume_review, name='request-resume-review'),
    path('resume-reviews/', views.resume_review_list, name='resume-review-list'),
]
