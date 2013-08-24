# coding: utf-8
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect, get_object_or_404

@login_required
def settings(request):
    return redirect('/settings/profile/')

@login_required
def profile(request):
    if request.method == 'POST':
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        email = request.POST['email']
        location = request.POST['location']
        institution = request.POST['institution']
        url = request.POST['url']

        user = request.user

        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        user.get_profile().location = location
        user.get_profile().institution = institution
        user.get_profile().url = url

        user.save()
        messages.add_message(request, messages.SUCCESS, 'Your profile were successfully edited.')
    context = RequestContext(request)
    return render_to_response('settings/profile.html', context)

@login_required
def password(request):
    if request.method == 'POST':
        old_password = request.POST['old-password']
        new_password = request.POST['new-password']
        confirm_new_password = request.POST['confirm-new-password']
        
        user = request.user

        if user.check_password(old_password):
            if new_password == confirm_new_password:
                user.set_password(new_password)
                user.save()
                messages.add_message(request, messages.SUCCESS, 'Your password were successfully changed.')
            else:
                messages.add_message(request, messages.ERROR, 'The new password didn\'t match.')
        else:
            messages.add_message(request, messages.ERROR, 'The old password didn\'t match.')
    context = RequestContext(request)
    return render_to_response('settings/password.html', context)