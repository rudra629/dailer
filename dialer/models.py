# dialer/models.py
from django.db import models

class Lead(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('calling', 'Calling In Progress'),
        ('interested', 'Yes - Interested'),
        ('not_interested', 'No - Not Interested'),
        ('failed', 'Call Failed / Unanswered'),
    )
    
    phone_number = models.CharField(max_length=15, unique=True)
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.phone_number} - {self.status}"

class CallLog(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='call_logs')
    telecom_call_id = models.CharField(max_length=100, unique=True) 
    recording_url = models.URLField(max_length=500, blank=True, null=True)
    full_transcript = models.TextField(blank=True, null=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Log: {self.lead.phone_number}"