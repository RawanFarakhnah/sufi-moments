from django.urls import path
from sufi_app import views

urlpatterns = [
    path('', views.root, name='root'),
]