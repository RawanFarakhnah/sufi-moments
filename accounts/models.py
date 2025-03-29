from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language

class User(AbstractUser):
    # Remove username field (use email instead)
    username = None
    email = models.EmailField(_('email address'), unique=True)
    
    # English name fields
    first_name_en = models.CharField(_('first name (English)'), max_length=30, blank=True)
    last_name_en = models.CharField(_('last name (English)'), max_length=150, blank=True)
    
    # Arabic name fields
    first_name_ar = models.CharField(_('first name (Arabic)'), max_length=30, blank=True)
    last_name_ar = models.CharField(_('last name (Arabic)'), max_length=150, blank=True)
    
    # Admin flag
    is_admin = models.BooleanField(_('admin status'), default=False)
    
    # Set email as the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name_en', 'last_name_en']  # English names required for registration
    
    def __str__(self):
        """Returns the appropriate name based on current language"""
        if get_language() == 'ar' and self.first_name_ar and self.last_name_ar:
            return f"{self.first_name_ar} {self.last_name_ar}"
        return f"{self.first_name_en} {self.last_name_en}"
    
    def get_full_name(self):
        """Override to return bilingual names"""
        lang = get_language()
        if lang == 'ar' and self.first_name_ar and self.last_name_ar:
            return f"{self.first_name_ar} {self.last_name_ar}"
        return f"{self.first_name_en} {self.last_name_en}"
    
    def get_short_name(self):
        """Override for bilingual short name"""
        lang = get_language()
        if lang == 'ar' and self.first_name_ar:
            return self.first_name_ar
        return self.first_name_en

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')