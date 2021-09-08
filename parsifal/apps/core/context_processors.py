from django.conf import settings as django_settings

import parsifal


def settings(request):
    return {
        "parsifal_version": parsifal.__version__,
        "parsifal_release": django_settings.PARSIFAL_RELEASE,
        "parsifal_environment": django_settings.PARSIFAL_ENVIRONMENT,
        "recaptcha_enabled": django_settings.GOOGLE_RECAPTCHA_ENABLED,
        "recaptcha_site_key": django_settings.GOOGLE_RECAPTCHA_SITE_KEY,
        "google_analytics_ua": django_settings.GOOGLE_ANALYTICS_UA,
        "sentry_dsn": django_settings.SENTRY_DSN,
    }
