from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from .models import Event, EventType, Rsvp
from .forms import EventForm, RsvpForm
from django.db.models import Q

# Event Type Views
class EventTypeListView(ListView):
    model = EventType
    template_name = 'events/eventtype_list.html'
    context_object_name = 'types'

class EventTypeDetailView(DetailView):
    model = EventType
    template_name = 'events/eventtype_detail.html'
    context_object_name = 'type'

class EventTypeCreateView(LoginRequiredMixin, CreateView):
    model = EventType
    fields = ['type_name_en', 'type_name_ar', 'description_en', 'description_ar']
    template_name = 'events/eventtype_form.html'
    success_url = reverse_lazy('events:type_list')

    def form_valid(self, form):
        messages.success(self.request, _('Event type created successfully!'))
        return super().form_valid(form)

class EventTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = EventType
    fields = ['type_name_en', 'type_name_ar', 'description_en', 'description_ar']
    template_name = 'events/eventtype_form.html'
    success_url = reverse_lazy('events:type_list')

    def form_valid(self, form):
        messages.success(self.request, _('Event type updated successfully!'))
        return super().form_valid(form)

class EventTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = EventType
    template_name = 'events/eventtype_confirm_delete.html'
    success_url = reverse_lazy('events:type_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Event type deleted successfully!'))
        return super().delete(request, *args, **kwargs)

# Event Views
class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        event_type = self.request.GET.get('type')
        
        if search_query:
            queryset = queryset.filter(
                Q(name_en__icontains=search_query) | 
                Q(name_ar__icontains=search_query) |
                Q(description_en__icontains=search_query) |
                Q(description_ar__icontains=search_query)
            )
        
        if event_type:
            queryset = queryset.filter(event_type_id=event_type)
        
        return queryset.order_by('-event_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_types'] = EventType.objects.all()
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        
        # Check if user has RSVP'd
        if self.request.user.is_authenticated:
            try:
                context['user_rsvp'] = Rsvp.objects.get(
                    user=self.request.user, 
                    event=event
                )
            except Rsvp.DoesNotExist:
                context['user_rsvp'] = None
        
        # Get RSVP counts
        context['going_count'] = event.rsvps.filter(status='going').count()
        context['interested_count'] = event.rsvps.filter(status='interested').count()
        
        return context

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:event_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, _('Event created successfully!'))
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'

    def get_success_url(self):
        return reverse_lazy('events:event_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, _('Event updated successfully!'))
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not request.user.is_superuser and obj.created_by != request.user:
            messages.error(request, _("You don't have permission to edit this event."))
            return redirect('events:event_detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)

class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('events:event_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Event deleted successfully!'))
        return super().delete(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not request.user.is_superuser and obj.created_by != request.user:
            messages.error(request, _("You don't have permission to delete this event."))
            return redirect('events:event_detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)

# RSVP Views
class RsvpView(LoginRequiredMixin, CreateView):
    model = Rsvp
    form_class = RsvpForm
    template_name = 'events/rsvp_form.html'

    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
        form.instance.user = self.request.user
        form.instance.event = event
        
        # Check if RSVP already exists
        if Rsvp.objects.filter(user=self.request.user, event=event).exists():
            messages.warning(self.request, _('You have already RSVP\'d for this event.'))
            return redirect('events:event_detail', pk=event.pk)
        
        messages.success(self.request, _('Thank you for your RSVP!'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('events:event_detail', kwargs={'pk': self.kwargs['event_pk']})

class RsvpUpdateView(LoginRequiredMixin, UpdateView):
    model = Rsvp
    form_class = RsvpForm
    template_name = 'events/rsvp_form.html'

    def get_object(self):
        event_pk = self.kwargs['event_pk']
        return get_object_or_404(Rsvp, user=self.request.user, event_id=event_pk)

    def form_valid(self, form):
        messages.success(self.request, _('RSVP updated successfully!'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('events:event_detail', kwargs={'pk': self.kwargs['event_pk']})

class RsvpDeleteView(LoginRequiredMixin, DeleteView):
    model = Rsvp
    template_name = 'events/rsvp_confirm_delete.html'

    def get_object(self):
        event_pk = self.kwargs['event_pk']
        return get_object_or_404(Rsvp, user=self.request.user, event_id=event_pk)

    def delete(self, request, *args, **kwargs):
        messages.success(request, _('RSVP removed successfully!'))
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('events:event_detail', kwargs={'pk': self.kwargs['event_pk']})

# Calendar View
# class EventCalendarView(ListView):
#     model = Event
#     template_name = 'events/event_calendar.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         events = Event.objects.filter(event_date__gte=timezone.now())
#         context['events'] = events
#         return context

#     def get(self, request, *args, **kwargs):
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             events = Event.objects.filter(
#                 event_date__gte=timezone.now()
#             ).values('id', 'name_en', 'name_ar', 'event_date', 'end_date', 'location')
#             return JsonResponse(list(events), safe=False)
#         return super().get(request, *args, **kwargs)