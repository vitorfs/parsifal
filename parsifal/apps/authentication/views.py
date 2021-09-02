from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext as _

from parsifal.apps.authentication.forms import SignUpForm


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if not form.is_valid():
            messages.add_message(
                request,
                messages.ERROR,
                _(
                    "There was some problems while creating your account. "
                    "Please review some fields before submiting again."
                ),
            )
            return render(request, "registration/signup.html", {"form": form})
        else:
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            User.objects.create_user(username=username, password=password, email=email)
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.add_message(request, messages.SUCCESS, _("Your account were successfully created."))
            return HttpResponseRedirect("/" + username + "/")
    else:
        return render(request, "registration/signup.html", {"form": SignUpForm()})
