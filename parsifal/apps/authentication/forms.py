from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _


def ForbiddenUsernamesValidator(value):
    forbidden_usernames = [
        "admin",
        "settings",
        "news",
        "about",
        "help",
        "signin",
        "signup",
        "signout",
        "terms",
        "privacy",
        "cookie",
        "new",
        "login",
        "logout",
        "administrator",
        "join",
        "account",
        "username",
        "root",
        "blog",
        "user",
        "users",
        "billing",
        "subscribe",
        "reviews",
        "review",
        "blog",
        "blogs",
        "edit",
        "mail",
        "email",
        "home",
        "job",
        "jobs",
        "contribute",
        "newsletter",
        "shop",
        "profile",
        "register",
        "auth",
        "authentication",
        "campaign",
        "config",
        "delete",
        "remove",
        "forum",
        "forums",
        "download",
        "downloads",
        "contact",
        "blogs",
        "feed",
        "faq",
        "intranet",
        "log",
        "registration",
        "search",
        "explore",
        "rss",
        "support",
        "status",
        "static",
        "media",
        "setting",
        "css",
        "js",
        "follow",
        "activity",
        "library",
    ]
    if value.lower() in forbidden_usernames:
        raise ValidationError(gettext("This is a reserved word."))


def InvalidUsernameValidator(value):
    if "@" in value or "+" in value or "-" in value:
        raise ValidationError(gettext("Enter a valid username."))


def UniqueEmailValidator(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError(gettext("User with this Email already exists."))


def UniqueUsernameIgnoreCaseValidator(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError(gettext("User with this Username already exists."))


class SignUpForm(forms.ModelForm):
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput())
    confirm_password = forms.CharField(label=_("Confirm your password"), widget=forms.PasswordInput())
    email = forms.CharField(label=_("Email"), required=True)

    class Meta:
        model = User
        exclude = ("last_login", "date_joined")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].validators.append(ForbiddenUsernamesValidator)
        self.fields["username"].validators.append(InvalidUsernameValidator)
        self.fields["username"].validators.append(UniqueUsernameIgnoreCaseValidator)
        self.fields["email"].validators.append(UniqueEmailValidator)

    def clean(self):
        super().clean()
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and password != confirm_password:
            self._errors["password"] = self.error_class([gettext("Passwords don't match")])
        return self.cleaned_data
