from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from directs.models import Message
from django.contrib.auth.models import User
from profil.models import Profil
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
import json
from django.views.decorators.http import require_http_methods


@login_required
def inbox(request):
    user = request.user
    messages = Message.get_message(user=request.user)
    active_direct = None
    directs = None
    profile = get_object_or_404(Profil, user=user)

    if messages:
        message = messages[0]
        active_direct = message['user'].username
        directs = Message.objects.filter(user=request.user, reciepient=message['user'])
        directs.update(is_read=True)

        for message in messages:
            if message['user'].username == active_direct:
                message['unread'] = 0
    context = {
        'directs':directs,
        'messages': messages,
        'active_direct': active_direct,
        'profile': profile,
    }
    return render(request, 'directs/direct.html', context)


@login_required
def Directs(request, username):
    user  = request.user
    messages = Message.get_message(user=user)
    active_direct = username
    directs = Message.objects.filter(user=user, reciepient__username=username)  
    directs.update(is_read=True)

    for message in messages:
            if message['user'].username == username:
                message['unread'] = 0
    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
    }
    return render(request, 'directs/direct.html', context)

def SendDirect(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    body = request.POST.get('body')

    if request.method == "POST":
        to_user = User.objects.get(username=to_user_username)
        Message.sender_message(from_user, to_user, body)
        return redirect('message')

def UserSearch(request):
    query = request.GET.get('q')
    context = {}
    if query:
        users = User.objects.filter(Q(username__icontains=query))

        # Paginator
        paginator = Paginator(users, 8)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

        context = {
            'users': users_paginator,
            }

    return render(request, 'directs/search.html', context)

def NewConversation(request, username):
    from_user = request.user
    body = ''
    try:
        to_user = User.objects.get(username=username)
    except Exception as e:
        return redirect('search-users')
    if from_user != to_user:
        Message.sender_message(from_user, to_user, body)
    return redirect('message')

@login_required
@csrf_exempt
def delete_chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        
        try:
            # Retrieve the User instance for the username provided.
            recipient = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponseBadRequest("User does not exist.")
        
        # Ensure the request.user is either the sender or the recipient of the message.
        Message.objects.filter(
            (Q(sender=request.user) & Q(reciepient=recipient)) | 
            (Q(sender=recipient) & Q(reciepient=request.user))
        ).delete()

        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)



@require_http_methods(["DELETE"])
def delete_message(request, message_id):
    try:
        message = Message.objects.get(pk=message_id, sender=request.user)
        message.delete()
        return JsonResponse({'message': 'Message deleted successfully'}, status=200)
    except Message.DoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)