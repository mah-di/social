from django.db import models
from django.urls.base import reverse
from Profiles.models import Profile
from django.core.validators import FileExtensionValidator

# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=2000)
    image = models.ImageField(upload_to='posts', blank=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    likes = models.ManyToManyField(Profile, blank=True, related_name='posts_liked')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:20]

    def get_preview(self):
        return f"{self.content[:200]}..." if self.is_more() else self.content

    def is_more(self):
        return True if len(self.content) > 200 else False

    def get_likes(self):
        return self.likes.all().count()

    def get_likers(self):
        return self.likes.all()

    def get_total_comments(self):
        return self.comments.all().count()

    def get_comments(self):
        return self.comments.all()

    def get_url(self):
        return reverse('posts:single_post', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('-created',)


class Comment(models.Model):
    post_obj = models.ForeignKey(Post, default=None, on_delete=models.CASCADE, related_name='comments')
    commentor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=800)
    likes = models.ManyToManyField(Profile, blank=True, related_name='comments_liked')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.commentor}--{self.body}--{self.pk}'

    def get_url(self):
        return reverse('posts:single_post', kwargs={'pk': self.post_obj.pk})

    def get_author(self):
        return self.post_obj.author
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        return self

    class Meta:
        ordering = ('-created',)
        

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liker = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.liker}-l'

    def get_url(self):
        return reverse('posts:single_post', kwargs={'pk': self.post.pk})

    def get_author(self):
        return self.post.author

    class Meta:
        ordering = ('-created',)