# dialer/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_leads, name='upload_leads'),
]