from django.shortcuts import render

from .forms import UserRegisterForm,LoginForm
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from profil.models import Profil
def login_view(request):
    error = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request,username = form.cleaned_data['username'],password = form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    if 'next' in request.GET:
                        return HttpResponseRedirect(request.GET.get('next'))
                    else:
                        return redirect('index')
                else:
                    error = 'User not active'
                    return render(request,'registration/login.html',{'error':error,"form": LoginForm()})

            else:
                error = 'Username or password entered incorrectly'
                return render(request,'registration/login.html',{'error':error,"form": LoginForm()})

        else:
            error = "The form was filled out incorrectly"
            return render(request,'registration/login.html',{'error':error,"form": LoginForm()})
    else:
        return render(request,'registration/login.html',{'error':error,"form": LoginForm()})
        



def user_create_view(request):
    error = ''
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password2'])  # Password is already validated
            new_user.save()
            # Redirect to login page after successful registration
            Profil.objects.create(user=new_user)
            return redirect('login')
        else:
            # No need for a separate error message, form.errors contains all validation errors
            return render(request, 'registration/signup.html', {'form': form})   
    else:
        # For a GET request, just display the empty registration form
        form = UserRegisterForm()
        return render(request, 'registration/signup.html', {'form': form})
