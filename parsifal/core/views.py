# coding: utf-8
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login, logout as django_logout

def login(request):
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
                messages.add_message(request, messages.ERROR, 'Sua conta está desativada.')
                context = RequestContext(request)
                return render_to_response('core/login.html', context)
        else:
            messages.add_message(request, messages.ERROR, 'Usuário ou senha inválido.')
            context = RequestContext(request)
            return render_to_response('core/login.html', context)
    else:
        context = RequestContext(request)
        return render_to_response('core/login.html', context)

def logout(request):
    django_logout(request)
    return redirect('/login/')