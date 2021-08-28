from django.db import models
from Profiles.models import Profile

# Create your models here.

ACTIONS = (
    ('like', 'like'),
    ('comment', 'comment'),
    ('request received', 'request received'),
    ('request accepted', 'request accepted'),
)

class Notification(models.Model):
    notifying = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='all_notifications')
    notifier = models.ForeignKey(Profile, on_delete=models.CASCADE)
    action = models.CharField(max_length=16, blank= True, choices=ACTIONS)
    body = models.CharField(max_length=200, blank= True)
    seen = models.BooleanField(default=False)
    tobe_shown = models.BooleanField(default= True)
    target_url = models.CharField(default='', blank= True, max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.notifier.slug} {self.body}'

    def save(self, *args, **kwargs):
        if self.seen == False:
            count = Notification.objects.filter(notifying= self.notifying, action= self.action, target_url= self.target_url).count()
            Notification.objects.filter(notifying= self.notifying, action= self.action, target_url= self.target_url).update(tobe_shown= False, seen= True)
            if count == 1:
                self.body = f'and {count} other {self.body}'
            elif count > 1:
                self.body = f'and {count} others {self.body}'

        return super().save(*args, **kwargs)

    
    class Meta:
        ordering = ('-created',)