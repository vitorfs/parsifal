# coding: utf-8
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect, get_object_or_404

def new(request):
    validate_form = True
    error_username = ''
    error_email = ''
    error_password = ''
    error_confirm_password = ''

    username = request.POST['username']
    if not username:
        error_username = 'Username is a required field.'
        validate_form = False
    else:
        exists_username = User.objects.filter(username=username)
        if exists_username:
            error_username = 'The username is already taken.'
            validate_form = False

    email = request.POST['email']
    if not email:
        error_email = 'Email is a required field.'
        validate_form = False
    else:
        exists_email = User.objects.filter(email=email)
        if exists_email:
            error_email = 'The email is already used.'
            validate_form = False

    password = request.POST['password']
    if not password:
        error_password = 'Password is a required field.'
        validate_form = False

    try:
        confirm_password = request.POST['confirm-password']
        if confirm_password != password:
            error_confirm_password = 'Password didn\'t match.'
            validate_form = False
    except:
        pass
    

    if validate_form:
        User.objects.create_user(username=username, password=password, email=email)
        user = authenticate(username=username, password=password)
        login(request, user)
        messages.add_message(request, messages.SUCCESS, 'Your account were successfully created.')
        return redirect('/' + username + '/')
    else:
        messages.add_message(request, messages.ERROR, 'There was some problems while creating your account. Please review some fields before submiting again.')
        new_user = User(username=username, email=email)
        context = RequestContext(request, {'new_user': new_user
            , 'error_username': error_username
            , 'error_email': error_email
            , 'error_password': error_password
            , 'error_confirm_password': error_confirm_password
        })
        return render_to_response('core/signup.html', context)