from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.index, name='home'),
    path('friends/', views.friends_list, name='friends_list'),
    path('friend-requests/', views.friend_requests, name='friend_requests'),
    path('sent-requests/', views.sent_requests, name='sent_requests'),
    path('add-friends/', views.add_friend, name='add_friends'),
    path('send-request/', views.send_request, name='send_request'),
    path('remove-friend/', views.remove_friend, name='remove_friend'),
    path('accept-request/', views.accept_request, name='accept'),
    path('remove-request/', views.remove_request, name='remove'),
    path('<slug>/', views.view_profile, name='profile'),
]