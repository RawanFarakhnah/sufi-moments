# sufi_moments/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static

# URLs that SHOULD NOT be language-prefixed
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),  # Language switcher endpoint
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# URLs that SHOULD be language-prefixed /en/ or /ar/
urlpatterns += i18n_patterns(
    path('', include('landing.urls')),         
    path('events/', include('events.urls')),    
    path('memories/', include('memories.urls')),
    prefix_default_language=False
)