from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, EventRegistration
from .forms import EventForm
from django.contrib import messages

from django.utils import timezone

def event_list(request):
    now = timezone.now()
    events = Event.objects.filter(event_date__gte=now).order_by('event_date')
    return render(request, 'events/event_list.html', {'events': events})

@login_required
def event_register(request, pk):
    event = get_object_or_404(Event, pk=pk)
    EventRegistration.objects.get_or_create(event=event, user=request.user)
    messages.success(request, f"Successfully registered for {event.title}")
    return redirect('event-list')
@login_required
def event_create(request):
    if request.user.role not in ['ALUMNI', 'ADMIN']:
        messages.error(request, "Only alumni and faculty can host events.")
        return redirect('event-list')
        
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, f"Event '{event.title}' created successfully!")
            return redirect('event-list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})
