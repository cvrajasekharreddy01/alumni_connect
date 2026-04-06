from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job-list'),
    path('post/', views.post_job, name='post-job'),
    path('<int:pk>/', views.job_detail, name='job-detail'),
]
