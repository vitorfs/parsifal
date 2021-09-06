from django.conf import settings as django_settings


def settings(request):
    return {
        "environment": django_settings.PARSIFAL_ENVIRONMENT,
        "recaptcha_enabled": django_settings.GOOGLE_RECAPTCHA_ENABLED,
        "recaptcha_site_key": django_settings.GOOGLE_RECAPTCHA_SITE_KEY,
    }
