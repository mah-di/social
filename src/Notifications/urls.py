from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('<pk>/', views.notified, name='notified'),
]