# dialer/views.py
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from .models import Lead
from .tasks import initiate_outbound_call

def upload_leads(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
        
        for index, row in df.iterrows():
            phone = str(row.get('phone', '')).strip()
            name = str(row.get('name', '')).strip()
            if phone:
                lead, created = Lead.objects.get_or_create(
                    phone_number=phone, defaults={'customer_name': name, 'status': 'pending'}
                )
                if created or lead.status == 'pending':
                    initiate_outbound_call.delay(lead.id) # Send to Celery
                    
        return HttpResponse("Upload successful. Dialing engine started.")
    return render(request, 'dialer/upload.html')