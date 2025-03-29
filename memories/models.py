from django.db import models
from accounts.models import User
from django.utils.translation import get_language

class Memory(models.Model):
    user = models.ForeignKey(User, related_name="memories", on_delete=models.CASCADE)
    title_en = models.CharField(max_length=200)
    title_ar = models.CharField(max_length=200)
    description_en = models.TextField()
    description_ar = models.TextField()
    memory_image_url = models.URLField(max_length=500, blank=True, null=True)
    memory_image = models.ImageField(upload_to='memories/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_memories', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
   
    @property
    def title(self):
        return getattr(self, f'title_{get_language()}')

    @property
    def description(self):
        return getattr(self, f'description_{get_language()}')

    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.likes.count()