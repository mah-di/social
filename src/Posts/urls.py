from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.feed, name='feed'),
    path('post-action/', views.like_unlike, name='like_unlike'),
    path('post/make-post/', views.make_post, name='make_post'),
    path('post/make-comment/', views.make_comment, name='make_comment'),
    path('post/<pk>/', views.PostDetailView.as_view(), name='single_post'),
    path('post/<pk>/update/', views.PostUpdateView.as_view(), name='update_post'),
    path('post/<pk>/delete/', views.PostDeleteView.as_view(), name='delete_post'),
    path('comment/<pk>/update/', views.CommentUpdateView.as_view(), name='update_comment'),
    path('comment/<pk>/delete/', views.CommentDeleteView.as_view(), name='delete_comment'),

    path('comment/new/', views.ajax_comment, name='ajax_comment'),
]