from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'events'

urlpatterns = [
    # Event Type URLs
    path('types/', views.EventTypeListView.as_view(), name='type_list'),
    path('types/create/', login_required(views.EventTypeCreateView.as_view()), name='type_create'),
    path('types/<int:pk>/', views.EventTypeDetailView.as_view(), name='type_detail'),
    path('types/<int:pk>/update/', login_required(views.EventTypeUpdateView.as_view()), name='type_update'),
    path('types/<int:pk>/delete/', login_required(views.EventTypeDeleteView.as_view()), name='type_delete'),
    
    # Event URLs
    path('', views.EventListView.as_view(), name='event_list'),
    path('create/', login_required(views.EventCreateView.as_view()), name='event_create'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('<int:pk>/update/', login_required(views.EventUpdateView.as_view()), name='event_update'),
    path('<int:pk>/delete/', login_required(views.EventDeleteView.as_view()), name='event_delete'),
    
    # RSVP URLs
    path('<int:event_pk>/rsvp/', login_required(views.RsvpView.as_view()), name='rsvp'),
    path('<int:event_pk>/rsvp/update/', login_required(views.RsvpUpdateView.as_view()), name='rsvp_update'),
    path('<int:event_pk>/rsvp/delete/', login_required(views.RsvpDeleteView.as_view()), name='rsvp_delete'),
    
    # Calendar View
    # path('calendar/', views.EventCalendarView.as_view(), name='event_calendar'),
]