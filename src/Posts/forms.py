from django import forms
from .models import Post, Comment

#  Forms

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content', 'image',)
        labels = {
            'content' : '',
            'image': '',
        }
        widgets = {
            'content' : forms.Textarea(attrs={'rows': 4, 'placeholder': "What's on your mind?"}),
            'image' : forms.FileInput(attrs={'style': 'margin: 20px 0'})
        }


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'placeholder': 'Write a comment..'}), label='')
    class Meta:
        model = Comment
        fields = ('body',)


class CommentUpdateForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write a comment..', 'id': 'comment_body'}), label='')
    class Meta:
        model = Comment
        fields = ('body',)