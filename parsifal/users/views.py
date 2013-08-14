# coding: utf-8
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect, get_object_or_404

def new(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    User.objects.create_user(username=username, password=password, email=email)
    user = authenticate(username=username, password=password)
    login(request, user)
    messages.add_message(request, messages.SUCCESS, 'Your account were successfully created.')
    return redirect('/' + username + '/')

@login_required
def edit(request):
    if request.method == 'POST':
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        email = request.POST['email']
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Your profile were successfully edited.')
        return redirect('/' + request.user.username + '/')
    else:
        context = RequestContext(request)
        return render_to_response('users/edit.html', context)