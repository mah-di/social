from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import Post, Like, Comment
from Notifications.models import Notification
from django.urls.base import reverse

@receiver(post_save, sender=Like)
def add_post_like(sender, instance, created, **kwargs):
    post = instance.post
    liker = instance.liker

    post.likes.add(liker)

@receiver(post_delete, sender=Like)
def remove_post_like(sender, instance, **kwargs):
    post = instance.post
    liker = instance.liker

    post.likes.remove(liker)

@receiver(post_save, sender=Comment)
def new_comment_notify(sender, instance, created, **kwargs):
    if created:
        notifying = instance.get_author()
        notifier = instance.commentor

        if notifier != notifying:
            body = 'commented on your post.'
            target_url = reverse('posts:single_post', kwargs={'pk': instance.post_obj.pk})
            action = 'comment'

            notify = Notification(notifying= notifying, notifier= notifier, action=action, body= body, target_url= target_url)
            notify.save()

@receiver(post_save, sender=Like)
def new_like_notify(sender, instance, created, **kwargs):
    if created:
        notifying = instance.get_author()
        notifier = instance.liker

        if notifier != notifying:
            body = 'liked your post.'
            target_url = reverse('posts:single_post', kwargs={'pk': instance.post.pk})
            action = 'like'

            notify = Notification(notifying= notifying, notifier= notifier, action=action, body= body, target_url= target_url)
            notify.save()
