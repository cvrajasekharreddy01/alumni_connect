from django.urls import path
from . import views

urlpatterns = [
    path('alumni/', views.alumni_list, name='alumni-list'),
    path('detail/<int:pk>/', views.alumni_detail, name='alumni-detail'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('verify-alumni/<int:pk>/', views.verify_alumni, name='verify-alumni'),
    path('export-alumni-excel/', views.export_alumni_excel, name='export-alumni-excel'),
]
