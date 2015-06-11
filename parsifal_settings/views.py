# coding: utf-8

import os
from PIL import Image

from django.core.urlresolvers import reverse as r
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect, get_object_or_404, render
from django.conf import settings as django_settings

from parsifal.decorators import ajax_required
from parsifal_settings.forms import ProfileForm


@login_required
def settings(request):
    return redirect('/settings/profile/')

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, u'Your profile were successfully edited.')
            return redirect(r('settings:profile'))
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'settings/profile.html', { 'form': form })

@login_required
def picture(request):
    uploaded_picture = False
    try:
        if request.GET['upload_picture'] == 'uploaded':
            uploaded_picture = True
    except Exception, e:
        uploaded_picture = False
    return render(request, 'settings/picture.html', { 'uploaded_picture': uploaded_picture })


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


@login_required
def upload_picture(request):
    f = request.FILES['picture']
    filename = django_settings.MEDIA_ROOT + '/profile_pictures/' + request.user.username + '_tmp.jpg'
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)    
    im = Image.open(filename)
    width, height = im.size
    if width > 560:
        new_width = 560
        new_height = (height * 560) / width
        new_size = new_width, new_height
        im.thumbnail(new_size, Image.ANTIALIAS)
        im.save(filename)
    return redirect('/settings/picture/?upload_picture=uploaded')


@login_required
def save_uploaded_picture(request):
    try:
        x = int(request.POST['x'])
        y = int(request.POST['y'])
        w = int(request.POST['w'])
        h = int(request.POST['h'])
        tmp_filename = django_settings.MEDIA_ROOT + '/profile_pictures/' + request.user.username + '_tmp.jpg'
        filename = django_settings.MEDIA_ROOT + '/profile_pictures/' + request.user.username + '.jpg'
        im = Image.open(tmp_filename)
        cropped_im = im.crop((x, y, w+x, h+y))
        cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
        cropped_im.save(filename)
        os.remove(tmp_filename)
        return HttpResponse(django_settings.MEDIA_URL + 'profile_pictures/' + request.user.username + '.jpg')
    except Exception, e:
        return HttpResponseBadRequest()