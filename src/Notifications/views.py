from django.shortcuts import redirect, render
from .models import Notification

# Create your views here.

def notified(request, pk):
    noti = Notification.objects.get(pk=pk)
    noti.seen = True
    noti.save()

    return redirect(noti.target_url)