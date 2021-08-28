from django.shortcuts import render, redirect
from django.urls.base import reverse
from django.views.generic.detail import DetailView
from .models import Comment, Post, Like
from Profiles.models import Profile
from .forms import PostForm, CommentForm, CommentUpdateForm
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.timesince import timesince
from django.core.paginator import Paginator

# Create your views here.

def feed(request):
    posts = Post.objects.all()
    post_form = PostForm()
    comment_form = CommentForm()

    return render(request, 'Posts/feed.html', context={'posts': posts, 'post_form': post_form, 'comment_form': comment_form})

def make_post(request):
    profile = request.user.profile
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)

        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = profile
            new_post.save()
            messages.success(request, 'Post Added!')
    
    return redirect(request.META['HTTP_REFERER'])

def make_comment(request):
    profile = request.user.profile
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)    
            post_pk = request.POST.get('post_pk')
            new_comment.post_obj = Post.objects.get(pk=post_pk)
            new_comment.commentor = profile
            new_comment.save()
            messages.success(request, 'Comment Added!')
        

    return redirect(request.META['HTTP_REFERER'])

def like_unlike(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(pk=post_id)
        profile = request.user.profile
        unlike , like = Like.objects.get_or_create(post=post, liker=profile)

        if like is False:
            unlike.delete()

        response_data = {
            'likes' : post.likes.all().count(),
        }

        return JsonResponse(response_data, safe=False)

    return redirect(request.META['HTTP_REFERER'])


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'Posts/update_delete.html'
    success_url = reverse_lazy('posts:feed')

    def get_context_data(self, **kwargs):
        ctx =  super().get_context_data(**kwargs)
        ctx['request_type'] = 'update'
        ctx['obj_type'] = 'post'
        return ctx

    def get_object(self, *args, **kwargs):
        obj = super().get_object( *args, **kwargs)
        if self.request.user != obj.author.user:
            messages.warning(self.request, "You don't have access to the requested page.")
            return None
        
        return obj
    
    def form_valid(self, form):
        messages.info(self.request, 'Post updated!')
        return super().form_valid(form)


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'Posts/update_delete.html'
    success_url = reverse_lazy('posts:feed')

    def get_context_data(self, **kwargs):
        ctx =  super().get_context_data(**kwargs)
        ctx['request_type'] = 'delete'
        ctx['obj_type'] = 'post'
        return ctx

    def get_object(self, *args, **kwargs):
        obj = super().get_object( *args, **kwargs)
        if self.request.user != obj.author.user:
            messages.warning(self.request, "You don't have access to the requested page.")
            return None
        
        return obj

    def delete(self, request, *args: str, **kwargs):
        messages.info(self.request, 'Post deleted!')
        return super().delete(request, *args, **kwargs)


class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentUpdateForm
    template_name = 'Posts/update_delete.html'
    success_url = reverse_lazy('posts:feed')

    def get_context_data(self, **kwargs):
        ctx =  super().get_context_data(**kwargs)
        ctx['request_type'] = 'update'
        ctx['obj_type'] = 'comment'
        return ctx

    def get_object(self, *args, **kwargs):
        obj = super().get_object( *args, **kwargs)
        if self.request.user != obj.commentor.user:
            messages.warning(self.request, "You don't have access to the requested page.")
            return None
        
        return obj
    
    def form_valid(self, form):
        messages.info(self.request, 'Comment updated!')
        return super().form_valid(form)


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'Posts/update_delete.html'

    def get_context_data(self, **kwargs):
        ctx =  super().get_context_data(**kwargs)
        ctx['request_type'] = 'delete'
        ctx['obj_type'] = 'comment'
        return ctx

    def get_object(self, *args, **kwargs):
        obj = super().get_object( *args, **kwargs)
        if self.request.user != obj.commentor.user:
            messages.warning(self.request, "You don't have access to the requested page.")
            return None
        
        return obj

    def get_success_url(self):
        obj = self.get_object()
        return obj.get_url()

    def delete(self, request, *args: str, **kwargs):
        messages.info(self.request, 'Comment deleted!')
        return super().delete(request, *args, **kwargs)


class PostDetailView(DetailView):
    model = Post
    template_name = 'Posts/single_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comment_form'] = CommentForm()
        all_comments = Comment.objects.filter(post_obj= ctx['post'])
        comments = Paginator(all_comments, 2)
        ctx['comments'] = comments.get_page(1)
        return ctx


def ajax_comment(request):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)    
            profile = request.user.profile
            post_pk = request.POST.get('post_pk')
            post = Post.objects.get(pk=post_pk)
            new_comment.post_obj = post
            new_comment.commentor = profile
            comment = new_comment.save()
            comments = post.get_total_comments()
            response_data = {
                'result': 'success',
                'comments': comments,
                'update_button': reverse('posts:update_comment', kwargs={'pk': comment.pk}),
                'delete_button': reverse('posts:delete_comment', kwargs={'pk': comment.pk}),
                'commentor_avatar': comment.commentor.avatar.url,
                'commentor_profile': reverse('profiles:profile', kwargs={'slug': comment.commentor.slug}),
                'commentor_username': comment.commentor.user.username,
                'comment_created': timesince(comment.created)
            }
            return JsonResponse(response_data, safe=True)
        return JsonResponse({'result': 'error'}, safe=True)