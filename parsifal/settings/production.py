# flake8: noqa

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7 * 52  # one year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = True


# ==============================================================================
# EMAIL SETTINGS
# ==============================================================================

DEFAULT_FROM_EMAIL = "Parsifal Team <noreply@parsif.al>"
EMAIL_SUBJECT_PREFIX = "[Parsifal] "
SERVER_EMAIL = "application@parsif.al"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)


# ==============================================================================
# THIRD-PARTY APPS
# ==============================================================================

sentry_sdk.init(
    dsn=SENTRY_DSN,
    environment=PARSIFAL_ENVIRONMENT,
    release=PARSIFAL_RELEASE,
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.01,
    send_default_pii=True,
)
