from django.urls import path
from . import views

app_name = 'events'  # Add the app name here as the namespace

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/rsvp/', views.rsvp_create, name='rsvp_create'),
]