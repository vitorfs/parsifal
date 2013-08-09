# coding: utf-8
from django.contrib import messages
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def create_account(request):
  username = request.POST['username']
  password = request.POST['password']
  email = request.POST['email']
  User.objects.create_user(username=username, password=password, email=email)
  user = authenticate(username=username, password=password)
  login(request, user)
  messages.add_message(request, messages.SUCCESS, 'Your account were successfully created.')
  return redirect('/' + username + '/')