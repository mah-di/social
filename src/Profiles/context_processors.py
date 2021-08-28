from django.urls.base import reverse
from .models import Profile, Friendship

def get_user_profile(request):
    if request.user.is_authenticated:
        user_profile = request.user.profile

        return {'user_profile': user_profile}
    return {}

def get_friendship_stats(request):
    if request.user.is_authenticated:
        friend_requests_count = len(Friendship.objects.get_friend_requests(request.user.profile))
        sent_requests_count = len(Friendship.objects.get_sent_requests(request.user.profile))
        return {
            'friend_requests_count': friend_requests_count,
            'sent_requests_count': sent_requests_count,
        }
    return {}