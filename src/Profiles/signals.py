from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.contrib.auth.models import User
from .models import Friendship, Profile
from Notifications.models import Notification
from django.urls.base import reverse

@receiver(post_save, sender=User)
def post_save_profile_tune(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, slug=instance.username)
    
    else:
        pf = Profile.objects.get(user=instance)
        if pf.slug != instance.username:
            pf.slug = instance.username
            pf.save()

@receiver(post_save, sender=Friendship)
def post_save_fship_and_notification_update(sender, instance, created, **kwargs):
    if instance.status == 'accepted':
        req_sender = instance.sender
        req_receiver = instance.receiver
        req_sender.friends.add(req_receiver)
        req_receiver.friends.add(req_sender)
        req_sender.save()
        req_receiver.save()

        body = 'accepted your friend request.'
        target_url = reverse('profiles:profile', kwargs={'slug': req_receiver.slug})
        action = 'request accepted'
        notify = Notification(notifying= req_sender, notifier= req_receiver, action=action, body= body, target_url= target_url)
        notify.save()

@receiver(post_delete, sender=Friendship)
def post_delete_fship_update(sender, instance, **kwargs):
    req_sender = instance.sender
    req_receiver = instance.receiver
    req_sender.friends.remove(req_receiver)
    req_receiver.friends.remove(req_sender)
    req_sender.save()
    req_receiver.save()

@receiver(post_save, sender= Friendship)
def notifying_new_request(sender, instance, created, **kwargs):
    if created:
        req_sender = instance.sender
        req_receiver = instance.receiver
        
        body = 'sent you a friend request.'
        target_url = reverse('profiles:friend_requests')
        action = 'request received'
        notify = Notification(notifying= req_receiver, notifier= req_sender, action=action, body= body, target_url= target_url)
        notify.save()