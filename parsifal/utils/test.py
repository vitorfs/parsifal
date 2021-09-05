from django.conf import settings
from django.shortcuts import resolve_url
from django.utils.http import urlencode


def login_redirect_url(url):
    """
    Utility function to be used as the "expected_url" param of the
    test case assertRedirects.

    :param url: Model instance, url pattern, url
    :return: String in the format "/login/?next=%2Fabout%2F"
    """
    login_url = resolve_url(settings.LOGIN_URL)
    next_url = urlencode({"next": resolve_url(url)})
    return f"{login_url}?{next_url}"
