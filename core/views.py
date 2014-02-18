# coding: utf-8
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from reviews.models import Review
from utils.string import remove_accents
from core.forms import SignUpForm

def home(request):
    if request.user.is_authenticated():
        user_reviews = Review.objects.filter(author__id=request.user.id).order_by('-last_update',)
        context = RequestContext(request, {'user_reviews': user_reviews})
        return render_to_response('core/home.html', context)
    else:
        context = RequestContext(request)
        return render_to_response('core/cover.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'There was some problems while creating your account. Please review some fields before submiting again.')
            context = RequestContext(request, {'form': form})
            return render_to_response('core/signup.html', context)
        else:
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, password=password, email=email)
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Your account were successfully created.')
            return HttpResponseRedirect('/' + username + '/')
    else:
        context = RequestContext(request,  {'form': SignUpForm() })
        return render_to_response('core/signup.html', context)


def signin(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if 'next' in request.GET:
                        return HttpResponseRedirect(request.GET['next'])
                    else:
                        return HttpResponseRedirect('/')
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
    return HttpResponseRedirect('/')

def news(request):
    context = RequestContext(request)
    return render_to_response('core/news.html', context)

def about(request):
    context = RequestContext(request)
    return render_to_response('core/about.html', context)

def help(request):
    context = RequestContext(request)
    return render_to_response('core/help.html', context)