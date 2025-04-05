from django.urls import path
from . import views

app_name = 'memories'

urlpatterns = [
    path('', views.memory_list, name='list'),
    path('create/', views.memory_create, name='memory_create'),
    path('<int:pk>/', views.memory_detail, name='memory_detail'),
    path('<int:pk>/update/', views.memory_update, name='memory_update'),
    path('<int:pk>/delete/', views.memory_delete, name='memory_delete'),
    path('<int:pk>/like/', views.toggle_like, name='toggle_like'),
]