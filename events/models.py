from django.db import models
from accounts.models import User
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

class EventType(models.Model):
    type_name_en = models.CharField(_('type name (English)'), max_length=100)
    type_name_ar = models.CharField(_('type name (Arabic)'), max_length=100)
    description_en = models.TextField(_('description (English)'))
    description_ar = models.TextField(_('description (Arabic)'))

    def __str__(self):
        if get_language() == 'ar' and self.type_name_ar:
            return self.type_name_ar
        return self.type_name_en

    def get_description(self):
        if get_language() == 'ar' and self.description_ar:
            return self.description_ar
        return self.description_en

class Event(models.Model):
    # English fields
    name_en = models.CharField(_('name (English)'), max_length=255)
    description_en = models.TextField(_('description (English)'))
    
    # Arabic fields
    name_ar = models.CharField(_('name (Arabic)'), max_length=255, blank=True)
    description_ar = models.TextField(_('description (Arabic)'), blank=True)
    
    # Common fields (don't need translation)
    event_by = models.CharField(_('organized by'), max_length=255)
    event_date = models.DateTimeField(_('start date'))
    end_date = models.DateTimeField(_('end date'))
    location = models.CharField(_('location'), max_length=255)
    event_type = models.ForeignKey(EventType, related_name="events", 
                                 on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(_('image'), upload_to='events/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def name(self):
        from django.utils.translation import get_language
        if get_language() == 'ar' and self.name_ar:
            return self.name_ar
        return self.name_en

    @property
    def description(self):
        from django.utils.translation import get_language
        if get_language() == 'ar' and self.description_ar:
            return self.description_ar
        return self.description_en

    @property
    def duration(self):
        delta = self.end_date - self.event_date
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        # Translated duration string
        from django.utils.translation import gettext as _
        return _("{hours} hr {minutes} min").format(hours=hours, minutes=minutes)

    def __str__(self):
        return self.name  # Uses the language-aware property


class Rsvp(models.Model):
    STATUS_CHOICES = [
        ('going', _('Going')),
        ('interested', _('Interested')),
        ('not_going', _('Not Going')),
    ]

    user = models.ForeignKey(User, related_name="rsvps", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name="rsvps", on_delete=models.CASCADE)
    status = models.CharField(_('status'), max_length=10, 
                            choices=STATUS_CHOICES, default='interested')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'event']
        verbose_name = _('RSVP')
        verbose_name_plural = _('RSVPs')
    
    def get_status_display(self):
        """Returns the human-readable status label."""
        status_dict = dict(self.STATUS_CHOICES)
        return status_dict.get(self.status, self.status)


    def __str__(self):
        from django.utils.translation import gettext as _
        return _("{user} RSVP'd for {event} as {status}").format(
            user=self.user.get_short_name(),
            event=self.event.name,
            status=self.get_status_display()
        )