from django.db import models
import bcrypt
import re

# Create your models here.
class UserManger(models.Manager):
    def registor_validator(self, postData):
        errors = {}
        if len(postData.get('first_name')) < 2 or not postData.get('first_name').isalpha():
           errors['first_name'] = "First name should be at least 2 characters and only alphabetic."

        if len(postData.get('last_name')) < 2 or not postData.get('first_name').isalpha():
           errors['last_name'] = "Last name should be at least 2 characters and only alphabetic."

        EMAILREGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not EMAILREGEX.match(postData.get('email')):
           errors['email'] = "Enter a valid email (eg. user@example.com)"

        if not len(postData.get('password')) >= 8:
           errors['password'] = "Password should be at least 8 characters."
        
        if not postData.get('password') == postData.get('confirm_password'):
           errors['confirm_password'] = "Password  not match, please confirm password."
        
        return errors
        
    def login_validator(self, postData):
        errors = {}
        try:
            this_user = User.objects.get(email=postData['email'])
            if not bcrypt.checkpw(postData['password'].encode(), this_user.password.encode()):
                errors['login_validate'] = "Email or Password is not correct"
        except User.DoesNotExist:
            errors['DoesNotExist'] = "Email or Password is not correct"
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=512)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManger()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Memory(models.Model):
    memory_title = models.CharField(max_length=255)
    memory_description = models.TextField()
    memory_image_url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.memory_title
    
class EventType(models.Model):
    type_name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.type_name

class Event(models.Model):
    name = models.CharField(max_length=255)
    event_by = models.CharField(max_length=255)
    description = models.TextField()
    event_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    event_type = models.ForeignKey(EventType, related_name="events", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def duration(self):
      # Calculate the duration
      delta = self.end_date - self.event_date
      hours, remainder = divmod(delta.seconds, 3600)
      minutes, _ = divmod(remainder, 60)

      # Format the duration as "X hr Y min"
      return f"{hours} hr {minutes} min"

    def __str__(self):
        return self.name
    
class Rsvp(models.Model):
    STATUS_CHOICES = [
        ('going', 'Going'),
        ('interested', 'Interested'),
        ('not_going', 'Not Going'),
    ]

    user = models.ForeignKey(User, related_name="rsvps", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name="rsvps", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='interested')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.first_name} RSVP'd for {self.event.name} as {self.status}"

