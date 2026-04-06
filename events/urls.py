from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event-list'),
    path('register/<int:pk>/', views.event_register, name='event-register'),
    path('create/', views.event_create, name='event-create'),
]
