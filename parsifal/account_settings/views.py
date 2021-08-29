import os

from django.conf import settings as django_settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse as r

from PIL import Image

from parsifal.account_settings.forms import PasswordForm, ProfileForm, UserEmailForm


@login_required
def settings(request):
    return redirect("/settings/profile/")


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile were successfully edited.")
            return redirect(r("settings:profile"))
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, "settings/profile.html", {"form": form})


@login_required
def picture(request):
    uploaded_picture = False
    try:
        if request.GET["upload_picture"] == "uploaded":
            uploaded_picture = True
    except Exception:
        uploaded_picture = False
    return render(request, "settings/picture.html", {"uploaded_picture": uploaded_picture})


@login_required
def emails(request):
    if request.method == "POST":
        form = UserEmailForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Email changed successfully.")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = UserEmailForm(instance=request.user)
    return render(request, "settings/emails.html", {"form": form})


@login_required
def password(request):
    if request.method == "POST":
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password changed successfully.")
            update_session_auth_hash(request, form.user)
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordForm(request.user)
    return render(request, "settings/password.html", {"form": form})


@login_required
def upload_picture(request):
    try:
        f = request.FILES["picture"]
        ext = os.path.splitext(f.name)[1].lower()
        valid_extensions = [".gif", ".png", ".jpg", ".jpeg", ".bmp"]
        if ext in valid_extensions:
            filename = f"{django_settings.MEDIA_ROOT}/profile_pictures/{request.user.username}_tmp.jpg"
            with open(filename, "wb+") as destination:
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
            return redirect("/settings/picture/?upload_picture=uploaded")
        else:
            messages.error(request, "Invalid file format.")
    except Exception:
        messages.error(request, "An expected error occurred.")
    return redirect("/settings/picture/")


@login_required
def save_uploaded_picture(request):
    try:
        x = int(request.POST["x"])
        y = int(request.POST["y"])
        w = int(request.POST["w"])
        h = int(request.POST["h"])
        tmp_filename = f"{django_settings.MEDIA_ROOT}/profile_pictures/{request.user.username}_tmp.jpg"
        filename = f"{django_settings.MEDIA_ROOT}/profile_pictures/{request.user.username}.jpg"
        im = Image.open(tmp_filename)
        cropped_im = im.crop((x, y, w + x, h + y))
        cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
        cropped_im.save(filename)
        os.remove(tmp_filename)
        image_url = f"{django_settings.MEDIA_URL}/profile_pictures/{request.user.username}.jpg"
        return HttpResponse(image_url)
    except Exception:
        return HttpResponseBadRequest()


@login_required
def connections(request):
    return render(request, "settings/connections.html")
