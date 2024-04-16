from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse, resolve
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.core.paginator import Paginator
from django.db import transaction
from django.contrib.auth.models import User
from .forms import ProfilUpdateForm, EmailChangeForm
from post.models import Post, Follow, Stream
from .models import Profil
from accaunt.forms import EditProfileForm



def UserProfile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profil.objects.get_or_create(user=user)[0]  # Ensure this refers to the correct 'user'
    url_name = resolve(request.path).url_name
    posts = Post.objects.none()  # Empty queryset as a starting point
    user_profile = request.user.profile
    is_mutual = Follow.objects.filter(follower=user_profile.user, following=user).exists() and Follow.objects.filter(follower=user, following=user_profile.user).exists()

    can_view_details = profile.public or is_mutual


    if url_name == 'profile':
        posts = Post.objects.filter(user=profile.user).order_by('-posted')
    elif url_name == 'profilefavourite':
        posts = profile.favourite.all()
    
    # Profile Stats
    posts_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()
    # count_comment = Comment.objects.filter(post=posts).count()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'profile':profile,
        'posts_count':posts_count,
        'following_count':following_count,
        'followers_count':followers_count,
        'posts_paginator':posts_paginator,
        'follow_status':follow_status,
        'can_view_details': can_view_details,
        # 'count_comment':count_comment,
    }
    return render(request, 'profile.html', context)

def EditProfile(request):
    user = request.user.id
    profile = Profil.objects.get(user__id=user)

    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            # Only update the image if a new image has been uploaded
            if 'image' in request.FILES:
                profile.image = form.cleaned_data.get('image')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.location = form.cleaned_data.get('location')
            profile.url = form.cleaned_data.get('url')
            profile.bio = form.cleaned_data.get('bio')
            profile.save()
            return redirect('profile', profile.user.username)
    else:
        form = EditProfileForm(instance=request.user.profile)

    context = {
        'form': form,
    }
    return render(request, 'editprofile.html', context)

def follow(request, username, option):
    user = request.user
    following = get_object_or_404(User, username=username)

    try:
        f, created = Follow.objects.get_or_create(follower=request.user, following=following)

        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following, user=request.user).all().delete()
        else:
            posts = Post.objects.all().filter(user=following)[:25]
            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=request.user, date=post.posted, following=following)
                    stream.save()
        return HttpResponseRedirect(reverse('profile', args=[username]))

    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[username]))




from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def setting(request):
    if request.method == 'POST':
        email_form = EmailChangeForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
        profil_form = ProfilUpdateForm(instance=request.user.profile)   
        # Handle Email Change Form
        if 'email' in request.POST:
            email_form = EmailChangeForm(request.POST, instance=request.user)
            if email_form.is_valid():
                email_form.save()
                return redirect('setting')
            profil_form = ProfilUpdateForm(instance=request.user.profile)
            password_form = PasswordChangeForm(request.user)
        # Handle Password Change Form
        elif 'old_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important for keeping the user logged in after password change
                return redirect('setting')
            email_form = EmailChangeForm(instance=request.user)
            profil_form = ProfilUpdateForm(instance=request.user.profile)
        # Handle Profile Update Form
        else:  # Assume profile update form
            profil_form = ProfilUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            form_to_validate = profil_form

        # Validate and save the appropriate form
        if form_to_validate.is_valid():
            form_to_validate.save()
            if form_to_validate == password_form:
                update_session_auth_hash(request, request.user)  # Keep the user logged in after password change
            return redirect('setting')  # Redirect to prevent resubmission
    else:
        email_form = EmailChangeForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
        profil_form = ProfilUpdateForm(instance=request.user.profile)
    
    context = {
        'email_form': email_form,
        'password_form': password_form,
        'profil_form': profil_form,
    }
    return render(request, 'settings.html', context)

