from django.conf import settings

import requests

from parsifal.utils.ipaddress import get_remote_ip_address


def recaptcha_is_valid(request):
    if settings.GOOGLE_RECAPTCHA_ENABLED:
        recaptcha_response = request.POST.get("g-recaptcha-response")
        data = {"secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY, "response": recaptcha_response}
        ip_address = get_remote_ip_address(request)
        if ip_address:
            data.update(remoteip=ip_address)
        response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data, timeout=10)
        result = response.json()
        return result["success"]
    return True
