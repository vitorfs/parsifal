# coding: utf-8
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login, logout as django_logout

def home(request):
    context = RequestContext(request)
    return render_to_response('core/home.html', context)

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                django_login(request, user)
                if 'next' in request.GET:
                    return redirect(request.GET['next'])
                else:
                    return redirect('/')
            else:
                messages.add_message(request, messages.ERROR, 'Your account is desactivated.')
                context = RequestContext(request)
                return render_to_response('core/signin.html', context)
        else:
            messages.add_message(request, messages.ERROR, 'Username or password invalid.')
            context = RequestContext(request)
            return render_to_response('core/signin.html', context)
    else:
        context = RequestContext(request)
        return render_to_response('core/signin.html', context)

def signout(request):
    django_logout(request)
    return redirect('/login/')