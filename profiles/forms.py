from django import forms
from .models import StudentProfile, AlumniProfile, PlacementDetails, CampusPlacement, Experience

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['full_name', 'roll_number', 'department', 'branch', 'graduation_year', 'skills', 'interests', 'career_interest', 'bio', 'resume']
        widgets = {
            'skills': forms.TextInput(attrs={'placeholder': 'Enter skills separated by commas'}),
            'interests': forms.Textarea(attrs={'rows': 3}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class AlumniProfileForm(forms.ModelForm):
    class Meta:
        model = AlumniProfile
        fields = ['full_name', 'roll_number', 'branch', 'graduation_year', 'campus_placed', 'skills', 'bio']
        widgets = {
            'skills': forms.TextInput(attrs={'placeholder': 'Enter skills separated by commas'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class CampusPlacementForm(forms.ModelForm):
    class Meta:
        model = CampusPlacement
        fields = ['company_name', 'job_role', 'ctc', 'placement_year']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company_name', 'job_role', 'ctc', 'start_date', 'end_date', 'is_current', 'experience_description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'experience_description': forms.Textarea(attrs={'rows': 3}),
        }

class PlacementDetailsForm(forms.ModelForm):
    class Meta:
        model = PlacementDetails
        fields = ['company', 'role', 'year', 'status']
