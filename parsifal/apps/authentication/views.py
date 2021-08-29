from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
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
            return render(request, "auth/signup.html", {"form": form})
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
        return render(request, "auth/signup.html", {"form": SignUpForm()})


def signin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    else:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if "next" in request.GET:
                        return HttpResponseRedirect(request.GET["next"])
                    else:
                        return HttpResponseRedirect("/")
                else:
                    messages.add_message(request, messages.ERROR, _("Your account is deactivated."))
                    return render(request, "auth/signin.html")
            else:
                messages.add_message(request, messages.ERROR, _("Username or password invalid."))
                return render(request, "auth/signin.html")
        else:
            return render(request, "auth/signin.html")


def signout(request):
    logout(request)
    return HttpResponseRedirect("/")


reset = PasswordResetView.as_view(
    template_name="auth/reset.html",
    email_template_name="auth/reset_email.html",
    subject_template_name="auth/reset_subject.txt",
    success_url=reverse_lazy("success"),
)


reset_confirm = PasswordResetConfirmView.as_view(
    template_name="auth/reset_confirm.html", success_url=reverse_lazy("signin")
)


def success(request):
    return render(request, "auth/success.html")