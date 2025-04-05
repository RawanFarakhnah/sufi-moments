from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
import bcrypt
import re

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name_en']) < 2:
            errors['first_name_en'] = "First name must be at least 2 characters"
        if len(postData['last_name_en']) < 2:
            errors['last_name_en'] = "Last name must be at least 2 characters"

        EMAIL_REGEX = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
        if not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = "Invalid email address"

        if User.objects.filter(email=postData['email']).exists():
            errors['email'] = "Email already exists"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"

        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Passwords do not match"

        return errors

    def get_by_natural_key(self, email):
        """Override to use email as the unique identifier."""
        return self.get(email=email)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email, password and other fields.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)  # Normalize the email
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def normalize_email(self, email):
        """
        Normalize the email by lowercasing it.
        """
        email = email.strip().lower()
        return email
       
class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name_en = models.CharField(_('first name (English)'), max_length=30, blank=True)
    last_name_en = models.CharField(_('last name (English)'), max_length=150, blank=True)
    first_name_ar = models.CharField(_('first name (Arabic)'), max_length=30, blank=True)
    last_name_ar = models.CharField(_('last name (Arabic)'), max_length=150, blank=True)
    is_admin = models.BooleanField(_('admin status'), default=False)
    objects = UserManager()
    
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