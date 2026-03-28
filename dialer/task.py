# dialer/tasks.py
from celery import shared_task
from django.utils import timezone
import requests
from .models import Lead, CallLog

@shared_task(bind=True, max_retries=3)
def initiate_outbound_call(self, lead_id):
    try:
        lead = Lead.objects.get(id=lead_id, status='pending')
        lead.status = 'calling'
        lead.save()
        
        # Replace with your actual SIP Provider's outbound API
        # Tell the provider to connect the call to your WebSocket URL
        payload = {
            "to": lead.phone_number,
            "from": "YOUR_140_NUMBER",
            "webhook_url": "wss://yourdomain.com/ws/audio/" # Points to your Consumer
        }
        
        # response = requests.post("https://api.sip-provider.com/make_call", json=payload)
        # data = response.json()
        
        CallLog.objects.create(
            lead=lead,
            telecom_call_id="mock_transaction_123", # data['transaction_id']
            started_at=timezone.now()
        )
        return f"Called {lead.phone_number}"
    except Exception as e:
        raise self.retry(exc=e, countdown=60)