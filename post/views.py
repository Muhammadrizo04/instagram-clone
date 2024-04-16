from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect

from post.models import Post, Tag, Follow, Stream, Likes
from django.contrib.auth.models import User
from post.forms import NewPostform
from profil.models import Profil, Relationship
from django.urls import resolve
from comment.models import Comment
from comment.forms import NewCommentForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from notification.models import Notification
# from post.models import Post, Follow, Stream




@login_required
def index(request):
    user = request.user
    all_users = User.objects.filter(is_staff=False)
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    profile, created = Profil.objects.get_or_create(user=user)
    user_profile = request.user.profile

    following_profiles = Profil.objects.filter(
        follower__follower=user_profile
    ).distinct()

    posts = Stream.objects.filter(user=user_profile.user)
    posts = Stream.objects.filter(user=user)
    group_ids = []

    for post in posts:
        group_ids.append(post.post_id)

    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')


    # Check like and save status for each post
    for post in post_items:
        post.is_liked = Likes.objects.filter(user=user, post=post).exists()
        post.is_saved = profile.favourite.filter(id=post.id).exists()

    query = request.GET.get('q')
    if query:
        users = User.objects.filter(Q(username__icontains=query))

        paginator = Paginator(users, 6)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

    context = {
        'post_items': post_items,
        'follow_status': follow_status,
        'profile': profile,
        'all_users': all_users,
        'following_profiles': following_profiles,
        # 'users_paginator': users_paginator,
    }
    return render(request, 'index.html', context)



@login_required
def NewPost(request):
    if request.method == "POST":
        form = NewPostform(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()

            tags = form.cleaned_data.get('tags').split(',')
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(title=tag_name.strip())
                new_post.tags.add(tag)
            
            return redirect(new_post.get_absolute_url())
    else:
        form = NewPostform()
    return render(request, 'newpost.html', {'form': form})

@login_required
def PostDetail(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-date')
    profile = Profil.objects.get(user=user)
    is_liked = Likes.objects.filter(user=request.user, post=post).exists()
    is_saved = profile.favourite.filter(id=post.id).exists()


    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('post-details', args=[post.id]))
    else:
        form = NewCommentForm()

    context = {
        'profile':profile,
        'post': post,
        'form': form,
        'comments': comments,
        'is_liked': is_liked,
        'is_saved': is_saved,
    }

    return render(request, 'postdetail.html', context)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    return redirect('profile')

@login_required
def Tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-posted')

    context = {
        'posts': posts,
        'tag': tag

    }
    return render(request, 'tag.html', context)


@login_required
def toggle_favorite(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        profile = get_object_or_404(Profil, user=request.user)
        is_saved = profile.favourite.filter(id=post.id).exists()

        if is_saved:
            profile.favourite.remove(post)
        else:
            profile.favourite.add(post)

        return JsonResponse({'is_saved': not is_saved})

    return JsonResponse({'error': 'Invalid request'}, status=400)

# Like function
@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()

    
    if not liked:
        Likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1
        Likes.objects.create(user=user, post=post)
        post.likes += 1
        # Create a "Like" notification
        Notification.objects.create(
            post=post,
            sender=user,
            user=post.user,
            notification_types=1,  # Assuming 1 represents a "Like"
            text_preview=f"{user.username} liked your post."
        )
    else:   
        Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1
        
    post.likes = current_likes
    post.save()
    # return HttpResponseRedirect(reverse('post-details', args=[post_id]))
    return JsonResponse({'liked': not liked, 'likes': post.likes})

@login_required
def favourite(request, post_id):
    if request.method == 'POST':
        user = request.user
        post = get_object_or_404(Post, id=post_id)
        profile = Profil.objects.get(user=user)
        isFavourite = False

        if profile.favourite.filter(id=post_id).exists():
            profile.favourite.remove(post)
        else:
            profile.favourite.add(post)
            isFavourite = True

        return JsonResponse({'isFavourite': isFavourite})

    # For non-POST requests, you can redirect or raise an error
    return JsonResponse({'error': 'Method not allowed'}, status=405)



def all_posts(request):
    posts = Post.objects.all().order_by('-posted')
    return render(request, 'posts.html', {'posts': posts})


from django.shortcuts import render

def error_404(request, exception):
    data = {}
    return render(request, '404.html', data)

def error_500(request):
    data = {}
    return render(request, '500.html', data)
