# coding: utf-8
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def home(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        return render_to_response('core/home.html', context)
    else:
        return render_to_response('core/cover.html', context)

def signin(request):
    if request.user.is_authenticated():
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
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
    logout(request)
    return redirect('/')

def news(request):
    context = RequestContext(request)
    return render_to_response('core/news.html', context)

def about(request):
    context = RequestContext(request)
    return render_to_response('core/about.html', context)

def help(request):
    context = RequestContext(request)
    return render_to_response('core/help.html', context)