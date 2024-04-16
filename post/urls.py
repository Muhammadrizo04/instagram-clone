from django.urls import path
from post.views import *
from django.conf.urls import handler404, handler500
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('posts/', all_posts, name='all-posts'),
    path('newpost', NewPost, name='newpost'),
    path('<uuid:post_id>', PostDetail, name='post-details'),
    path('tag/<slug:tag_slug>', Tags, name='tags'),
    path('like/<uuid:post_id>', like, name='like'),
    path('<uuid:post_id>/favourite', favourite, name='favourite'),
    path('post/delete/<uuid:post_id>/', delete_post, name='delete-post'),
    path('favorite/<uuid:post_id>', toggle_favorite, name='toggle-favorite'),
    path('post/<uuid:post_id>/', PostDetail, name='post-details'),
    
]
handler404 = 'post.views.error_404'
handler500 = 'post.views.error_500'
