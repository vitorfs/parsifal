import os

from django.conf import settings as django_settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView, TemplateView, UpdateView

from PIL import Image

from parsifal.apps.accounts.forms import ProfileForm, UserEmailForm


class SettingsRedirectView(LoginRequiredMixin, RedirectView):
    pattern_name = "settings:profile"


class UpdateProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = ProfileForm
    success_url = reverse_lazy("settings:profile")
    success_message = _("Your profile was updated with success!")
    template_name = "accounts/profile.html"

    def get_object(self, queryset=None):
        return self.request.user.profile


class UpdateEmailsView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = UserEmailForm
    success_url = reverse_lazy("settings:emails")
    success_message = _("Account email was updated with success!")
    template_name = "accounts/emails.html"

    def get_object(self, queryset=None):
        return self.request.user


class PictureView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/picture.html"

    def get_context_data(self, **kwargs):
        kwargs["uploaded_picture"] = self.request.GET.get("upload_picture") == "uploaded"
        return super().get_context_data(**kwargs)


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
            url = reverse("settings:picture")
            url = f"{url}?upload_picture=uploaded"
            return redirect(url)
        else:
            messages.error(request, "Invalid file format.")
    except Exception:
        messages.error(request, "An expected error occurred.")
    return redirect("settings:picture")


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
