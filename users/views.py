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

    if username == '' or password == '' or email == '':
      return redirect('/')
    
    unique_username = User.objects.filter(username=username)
    unique_email = User.objects.filter(email=email)

    if unique_username or unique_email:
      return redirect('/')

    User.objects.create_user(username=username, password=password, email=email)
    user = authenticate(username=username, password=password)
    login(request, user)
    messages.add_message(request, messages.SUCCESS, 'Your account were successfully created.')
    return redirect('/' + username + '/')
