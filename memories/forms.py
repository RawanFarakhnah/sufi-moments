from django import forms
from .models import Memory
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class MemoryForm(forms.ModelForm):
    # Make image_url optional if image is provided
    memory_image_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://example.com/image.jpg'
        }),
        label="رابط الصورة"
    )
    
    # Add file upload field
    memory_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        label="رفع صورة مباشرة"
    )

    class Meta:
        model = Memory
        fields = ['title_en', 'title_ar', 'description_en', 'description_ar', 'memory_image_url', 'memory_image']
        widgets = {
            'title_en': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Memory title (English)'
            }),
            'title_ar': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان الذكرى (عربي)'
            }),
            'description_en': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your memory details in English...'
            }),
            'description_ar': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'شاركنا تفاصيل ذكراك الجميلة بالعربية...'
            }),
        }
        labels = {
            'title_en': 'Title (English)',
            'title_ar': 'العنوان (عربي)',
            'description_en': 'Description (English)',
            'description_ar': 'الوصف (عربي)',
        }
        help_texts = {
            'memory_image_url': 'You can use a URL from Imgur or any image sharing service',
            'memory_image': 'Or upload an image directly from your device',
        }

    def clean(self):
        cleaned_data = super().clean()
        image_url = cleaned_data.get('memory_image_url')
        image_file = cleaned_data.get('memory_image')

        # Require at least one image source
        if not image_url and not image_file:
            raise ValidationError({
                'memory_image_url': 'You must provide either an image URL or upload an image',
                'memory_image': 'You must upload an image or provide an image URL'
            })

        # Validate URL if provided
        if image_url:
            validator = URLValidator()
            try:
                validator(image_url)
            except ValidationError:
                raise ValidationError({
                    'memory_image_url': 'Please enter a valid image URL'
                })

        return cleaned_data

    def save(self, commit=True):
        memory = super().save(commit=False)
        
        # Set the user from the request
        if hasattr(self, 'request'):
            memory.user = self.request.user

        if commit:
            memory.save()
        
        return memory