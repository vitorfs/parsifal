import re

from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext, gettext_lazy as _


def validate_forbidden_usernames(value):
    forbidden_usernames = {
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
        "reset",
        "sitemap.xml",
        "robots.txt",
        "review_settings",
        "password_change",
        "password_reset",
    }
    if value.lower() in forbidden_usernames:
        raise ValidationError(gettext("This is a reserved word."))


def validate_case_insensitive_email(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError(gettext("A user with that email already exists."))


def validate_case_insensitive_username(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError(gettext("A user with that username already exists."))


@deconstructible
class ASCIIUsernameValidator(validators.RegexValidator):
    regex = r"^[\w.]+\Z"
    message = _("Enter a valid username. This value may contain only English letters, numbers, and . _ characters.")
    flags = re.ASCII
