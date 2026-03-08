# urls.py
from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.NoteListAPIView.as_view(), name='note-list'),
    path('<int:pk>/', views.NoteDetailAPIView.as_view(), name='note-detail'),
    path('xss-vulnerable/', views.xss_vulnerable, name='xss_vulnerable'),
    path('xss-secure/', views.xss_secure, name='xss_secure'),
    path('sqli-vulnerable/', views.sqli_vulnerable, name='sqli_vulnerable'),
    path('sqli-secure/', views.sqli_secure, name='sqli_secure'),
    path('csrf-vulnerable/', views.csrf_vulnerable, name='csrf_vulnerable'),
    path('csrf-secure/', views.csrf_secure, name='csrf_secure'),
    path('env-demo/', views.env_demo, name='env_demo'),
]