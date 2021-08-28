from django.db.models.query_utils import Q
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from .models import Profile, Friendship
from .forms import ProfileUpdateForm, TestForm

# Create your views here.

def index(request):
    form = TestForm()
    ctx = {'name': request.path_info, 'form': form, 'url': reverse('profiles:profile', kwargs={'slug': 'super'}).lstrip('/') }

    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            ctx.update({'username': username})
            ctx.update({'email': email})
            ctx.update({'test': "yes"})

    return render(request, 'main/home.html', context=ctx)

def view_profile(request, slug):
    profile = Profile.objects.get(slug=slug)
    form = ProfileUpdateForm(instance=profile)


    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

    return render(request, 'Profiles/profile.html', context={'profile':profile, 'form':form})
    
def friends_list(request):
    profile = request.user.profile
    friends = profile.get_all_friends()

    return render(request, 'Profiles/friendship_lists.html', context={'friends': friends, 'q_type': 'friends'})

def friend_requests(request):
    profile = request.user.profile
    f_requests = Friendship.objects.get_friend_requests(profile)

    return render(request, 'Profiles/friendship_lists.html', context={'f_requests': f_requests, 'q_type': 'received'})

def sent_requests(request):
    profile = request.user.profile
    sent_requests = Friendship.objects.get_sent_requests(profile)

    return render(request, 'Profiles/friendship_lists.html', context={'sent_requests': sent_requests, 'q_type': 'sent'})

def add_friend(request):
    profiles = Profile.objects.get_profiles(request.user.profile)

    return render(request, 'Profiles/friendship_lists.html', context={'profiles': profiles, 'q_type': 'add_friends'})

def send_request(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        profile = request.user.profile
        sent_to = Profile.objects.get(pk=pk)

        send = Friendship(sender=profile, receiver= sent_to)
        send.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def accept_request(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        profile = request.user.profile
        sender = Profile.objects.get(pk=pk)

        f_req = Friendship.objects.get(sender= sender, receiver=profile)
        f_req.status = 'accepted'
        f_req.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_request(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        profile = request.user.profile
        p_friend = Profile.objects.get(pk=pk)

        Friendship.objects.filter((Q(sender= p_friend) & Q(receiver=profile)) | (Q(sender= profile) & Q(receiver=p_friend))).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_friend(request):
    if request.method == 'POST':
        pk = request.POST.get('friend_pk')
        me = request.user.profile
        friend = Profile.objects.get(pk=pk)
        Friendship.objects.filter((Q(sender=me) & Q(receiver=friend)) | (Q(sender=friend) & Q(receiver=me))).delete()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))