from django import forms
from django.utils import timezone
from .models import Event, Rsvp
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class EventForm(forms.ModelForm):
    # English Fields
    name_en = forms.CharField(
        label=_("Event Name (English)"),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description_en = forms.CharField(
        label=_("Description (English)"),
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    
    # Arabic Fields
    name_ar = forms.CharField(
        label=_("اسم الفعالية (عربي)"),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description_ar = forms.CharField(
        label=_("الوصف (عربي)"),
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )

    # DateTime Fields (common for both languages)
    event_date = forms.DateTimeField(
        label=_("Start Date/Time"),
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    end_date = forms.DateTimeField(
        label=_("End Date/Time"),
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )

    class Meta:
        model = Event
        fields = ['name_en', 'name_ar', 'description_en', 'description_ar', 'event_date', 'end_date', 'event_by', 'location', 'event_type', 'image']
        widgets = {
            'event_by': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        event_date = cleaned_data.get('event_date')
        end_date = cleaned_data.get('end_date')

        if event_date and end_date:
            if event_date < timezone.now():
                raise ValidationError({'event_date': _("Event date cannot be in the past")})
            
            if end_date <= event_date:
                raise ValidationError({'end_date': _("End time must be after start time")})

        return cleaned_data


class RsvpForm(forms.ModelForm):
    class Meta:
        model = Rsvp
        fields = ['status']
        widgets = {
            'status': forms.RadioSelect(attrs={'class': 'form-check-input'})
        }
        labels = {'status': _("Attendance Status")}
