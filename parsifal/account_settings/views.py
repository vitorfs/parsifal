# coding: utf-8

import os
from PIL import Image
from mendeley.session import MendeleySession
from oauthlib.oauth2 import TokenExpiredError
from dropbox.client import DropboxClient, DropboxOAuth2Flow

from django.core.urlresolvers import reverse as r
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.conf import settings as django_settings
from django.contrib.auth import update_session_auth_hash

from parsifal.account_settings.forms import UserEmailForm, ProfileForm, PasswordForm


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
def emails(request):
    if request.method == 'POST':
        form = UserEmailForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, u'Account Email changed successfully.')
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        form = UserEmailForm(instance=request.user)
    return render(request, 'settings/emails.html', { 'form' : form })

@login_required
def password(request):
    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, u'Password changed successfully.')
            update_session_auth_hash(request, form.user)
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'settings/password.html', { 'form' : form })


@login_required
def upload_picture(request):
    try:
        f = request.FILES['picture']
        ext = os.path.splitext(f.name)[1].lower()
        valid_extensions = ['.gif', '.png', '.jpg', '.jpeg', '.bmp']
        if ext in valid_extensions:
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
        else:
            messages.error(request, u'Invalid file format.')
    except Exception, e:
        messages.error(request, u'An expected error occurred.')
    return redirect('/settings/picture/')


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

def get_dropbox_auth_flow(session):
    return DropboxOAuth2Flow(
            django_settings.DROPBOX_APP_KEY,
            django_settings.DROPBOX_SECRET,
            django_settings.DROPBOX_REDIRECT_URI,
            session,
            'dropbox-auth-csrf-token')

@login_required
def connections(request):
    return render(request, 'settings/connections.html')

@login_required
def mendeley_connection(request):
    mendeley_profile = request.user.profile.get_mendeley_profile()
    mendeley_profile_picture = None
    if not mendeley_profile:
        mendeley = django_settings.MENDELEY
        auth = mendeley.start_authorization_code_flow()
        mendeley_auth_url = auth.get_login_url()
    else:
        mendeley_profile_picture = mendeley_profile.photo.square
        mendeley_profile_picture = mendeley_profile_picture.replace('http://', 'https://')
        mendeley_auth_url = ''
    return render(request, 'settings/includes/mendeley_connection.html', {
            'mendeley_auth_url': mendeley_auth_url,
            'mendeley_profile': mendeley_profile,
            'mendeley_profile_picture': mendeley_profile_picture
            })

@login_required
def dropbox_connection(request):
    dropbox_profile = request.user.profile.get_dropbox_profile()
    if not dropbox_profile:
        dropbox_auth_url = get_dropbox_auth_flow(request.session).start()
    else:
        dropbox_auth_url = ''
    return render(request, 'settings/includes/dropbox_connection.html', {
            'dropbox_auth_url': dropbox_auth_url,
            'dropbox_profile': dropbox_profile
            })

@login_required
def connect_mendeley(request):
    if 'code' in request.GET and 'state' in request.GET:
        code = request.GET.get('code')
        state = request.GET.get('state')
        mendeley = django_settings.MENDELEY
        auth = mendeley.start_authorization_code_flow(state=state)
        auth_path = u'{0}?code={1}&state={2}'.format(django_settings.MENDELEY_REDIRECT_URI, code, state)
        mendeley_session = auth.authenticate(auth_path)
        request.user.profile.set_mendeley_token(mendeley_session.token)
        request.user.save()
        messages.success(request, 'Your Mendeley account were linked successfully!')
    else:
        messages.error(request, 'A problem occurred while trying to connect your Mendeley account.')
    return redirect(r('settings:connections'))

@login_required
def disconnect_mendeley(request):
    if request.method == 'POST':
        request.user.profile.mendeley_token = None
        request.user.save()
        messages.success(request, 'Your Mendeley account were disconnected successfully!')
    return redirect(r('settings:connections'))

@login_required
def connect_dropbox(request):
    try:
        access_token, user_id, url_state = get_dropbox_auth_flow(request.session).finish(request.GET)
        messages.success(request, u'Your Dropbox account were linked successfully!')
        request.user.profile.dropbox_token = access_token
        request.user.save()
    except DropboxOAuth2Flow.NotApprovedException, e:
        messages.warning(request, 'You didn\'t approved Parsifal to connect your Dropbox account.')
    except Exception, e:
        messages.error(request, 'A problem occurred while trying to connect your Dropbox account. Please try again later.')
    return redirect(r('settings:connections'))

@login_required
def disconnect_dropbox(request):
    if request.method == 'POST':
        dropbox_token = request.user.profile.dropbox_token
        if dropbox_token is not None:
            client = DropboxClient(dropbox_token)
            client.disable_access_token()
            request.user.profile.dropbox_token = None
            request.user.save()
            messages.success(request, 'Your Dropbox account were disconnected successfully!')
    return redirect(r('settings:connections'))
