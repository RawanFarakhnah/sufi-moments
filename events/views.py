from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Event, Rsvp
from .forms import RsvpForm


# View to list all events
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/list.html', {'events': events})

# View to display details of a specific event
def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'events/detail.html', {'event': event})

# View to handle RSVP for an event
def rsvp_create(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = RsvpForm(request.POST)
        if form.is_valid():
            rsvp = form.save(commit=False)
            rsvp.event = event
            rsvp.user = request.user  # Assuming user is logged in
            rsvp.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = RsvpForm()
    return render(request, 'events/rsvp_create.html', {'form': form, 'event': event})

# View to list RSVPs for an event
# def event_rsvp_list(request, event_id):
#     event = get_object_or_404(Event, pk=event_id)
#     rsvps = Rsvp.objects.filter(event=event)
#     return render(request, 'events/event_rsvp_list.html', {'event': event, 'rsvps': rsvps})
