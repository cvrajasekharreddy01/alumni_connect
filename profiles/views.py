from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from users.models import User
from django.forms import inlineformset_factory
from django.contrib import messages
from .models import AlumniProfile, StudentProfile, CampusPlacement, Experience
import pandas as pd
from django.http import HttpResponse
from io import BytesIO
from .forms import StudentProfileForm, AlumniProfileForm, CampusPlacementForm, ExperienceForm

def alumni_list(request):
    alumni = AlumniProfile.objects.all()
    
    # Filter logic
    industry = request.GET.get('industry')
    company = request.GET.get('company')
    skills = request.GET.get('skills')
    branch = request.GET.get('branch')
    graduation_year = request.GET.get('graduation_year')

    if industry:
        alumni = alumni.filter(industry__icontains=industry)
    if company:
        alumni = alumni.filter(company__icontains=company)
    if skills:
        alumni = alumni.filter(skills__icontains=skills)
    if branch:
        alumni = alumni.filter(branch__icontains=branch)
    if graduation_year:
        alumni = alumni.filter(graduation_year=graduation_year)

    return render(request, 'profiles/alumni_list.html', {'alumni': alumni})

@login_required
def edit_profile(request):
    user = request.user
    if user.role == 'STUDENT':
        profile, created = StudentProfile.objects.get_or_create(user=user)
        if request.method == 'POST':
            form = StudentProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        else:
            form = StudentProfileForm(instance=profile)
    elif user.role == 'ALUMNI':
        profile, created = AlumniProfile.objects.get_or_create(user=user)
        placement, created = CampusPlacement.objects.get_or_create(alumni=profile)
        
        ExperienceFormSet = inlineformset_factory(
            AlumniProfile, Experience, form=ExperienceForm, 
            extra=1, can_delete=True
        )
        
        if request.method == 'POST':
            form = AlumniProfileForm(request.POST, instance=profile)
            placement_form = CampusPlacementForm(request.POST, instance=placement)
            formset = ExperienceFormSet(request.POST, instance=profile)
            
            if form.is_valid() and formset.is_valid():
                profile = form.save()
                if profile.campus_placed:
                    placement_form = CampusPlacementForm(request.POST, instance=placement)
                    if placement_form.is_valid():
                        placement_form.save()
                formset.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('dashboard')
        else:
            form = AlumniProfileForm(instance=profile)
            placement_form = CampusPlacementForm(instance=placement)
            formset = ExperienceFormSet(instance=profile)
            
        return render(request, 'profiles/edit_profile.html', {
            'form': form, 
            'placement_form': placement_form,
            'formset': formset
        })
    else:
        return redirect('dashboard')
        
    return render(request, 'profiles/edit_profile.html', {'form': form})

@login_required
def verify_alumni(request, pk):
    if request.user.role not in ['ADMIN', 'FACULTY']:
        messages.error(request, "You don't have permission to verify alumni.")
        return redirect('alumni-list')
    
    alumni_profile = get_object_or_404(AlumniProfile, pk=pk)
    alumni_profile.is_verified = True
    alumni_profile.save()
    
    from core.models import AuditLog
    AuditLog.objects.create(
        action_type='VERIFY_ALUMNI',
        performed_by=request.user,
        target_user=alumni_profile.user,
        description=f"Verified alumni: {alumni_profile.user.email}"
    )
    
    messages.success(request, f"Alumni {alumni_profile.user.email} has been verified.")
    return redirect('alumni-list')

@login_required
def export_alumni_excel(request):
    if request.user.role not in ['ADMIN', 'FACULTY']:
        messages.error(request, "You don't have permission to export data.")
        return redirect('alumni-list')
    
    alumni = AlumniProfile.objects.all()
    
    data = []
    for profile in alumni:
        placement = getattr(profile, 'campus_placement', None)
        experiences = profile.experiences.all()
        current_job = experiences.filter(is_current=True).first()
        
        data.append({
            'Email': profile.user.email,
            'Full Name': profile.full_name,
            'Roll Number': profile.roll_number,
            'Branch': profile.branch,
            'Graduation Year': profile.graduation_year,
            'Campus Placed': 'Yes' if profile.campus_placed else 'No',
            'Placement Company': placement.company_name if placement else 'N/A',
            'Placement CTC': placement.ctc if placement else 'N/A',
            'Current Company': current_job.company_name if current_job else 'N/A',
            'Current Role': current_job.job_role if current_job else 'N/A',
            'Verified': 'Yes' if profile.is_verified else 'No'
        })
    
    df = pd.DataFrame(data)
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Alumni')
    
    output.seek(0)
    
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=alumni_directory.xlsx'
    
    return response

def alumni_detail(request, pk):
    alumni = get_object_or_404(User, pk=pk, role='ALUMNI')
    
    # Increment views_count if viewer is not the profile owner
    if request.user.is_authenticated and request.user.pk != pk:
        profile = alumni.alumni_profile
        profile.views_count += 1
        profile.save(update_fields=['views_count'])
        
    return render(request, 'profiles/alumni_detail.html', {'profile_user': alumni})
