from django.db import models
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.urls.base import reverse


# Create your models here.

class ProfileManager(models.Manager):

    def get_profiles(self, my_profile):
        friends = my_profile.get_all_friends()
        received = Friendship.objects.get_friend_requests(my_profile)
        sent = Friendship.objects.get_sent_requests(my_profile)

        exclude = list(friends) + received + sent + [my_profile]
        exclude_users = []

        for item in exclude:
            exclude_users.append(item.user)

        return Profile.objects.exclude(user__in=exclude_users)

class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(default='avatar.png', upload_to='avatar/')
    bio = models.TextField(max_length=400, default='...')
    slug = models.SlugField(blank=True)
    friends = models.ManyToManyField('self', blank=True)
    country = models.CharField(max_length=200, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_url(self):
        return reverse('profiles:profile', kwargs={'slug': self.slug})

    def get_total_friends(self):
        return self.friends.all().count()

    def get_all_friends(self):
        return self.friends.all()

    def get_total_posts(self):
        return self.posts.all().count()

    def get_all_posts(self):
        return self.posts.all()

    def get_notifications(self):
        return self.all_notifications.all()

    def new_notifications(self):
        return self.all_notifications.filter(seen= False).count()

    def likes_given(self):
        return self.likes.all().count()

    def likes_gotten(self):
        posts = self.posts.all()
        likes = 0
        for post in posts:
            likes += post.likes.all().count()
        
        return likes

    def get_total_comments(self):
        return self.comments.all().count()

    def get_all_comments(self):
        return self.comments.all()

    def get_recent_comments(self):
        return self.comments.all()[:5]

    def get_all_posts_liked(self):
        return self.posts_liked.all()

    def get_recent_posts_liked(self):
        return self.posts_liked.all()[:5]

    def __str__(self):
        return f'{self.user.username}--{self.created.strftime("%d-%m-%Y")}'

class FriendshipManager(models.Manager):

    def get_friend_requests(self, profile):
        qs = Friendship.objects.filter(status='sent', receiver=profile)

        friends = []
        for fr in qs:
            friends.append(fr.sender)

        return friends

    def get_sent_requests(self, profile):
        qs = Friendship.objects.filter(status='sent', sender=profile)

        friends = []
        for fr in qs:
            friends.append(fr.receiver)

        return friends

REQUEST_STATUS= (
    ('sent', 'sent'),
    ('accepted', 'accepted'),
)

class Friendship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received')
    status = models.CharField(max_length=8, choices=REQUEST_STATUS, default=REQUEST_STATUS[0][0])
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = FriendshipManager()

    def __str__(self):
        return f'{self.sender}-->{self.receiver}==={self.status}'