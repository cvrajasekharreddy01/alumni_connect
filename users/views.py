from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user) # Don't login yet, wait for approval
            messages.success(request, 'Registration successful! Please wait for admin approval before logging in.')
            return redirect('approval-pending')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def approval_pending(request):
    return render(request, 'users/approval_pending.html')
