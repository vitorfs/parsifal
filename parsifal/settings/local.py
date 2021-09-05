# flake8: noqa

from .base import *

# ==============================================================================
# CORE SETTINGS
# ==============================================================================

INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")


# ==============================================================================
# EMAIL SETTINGS
# ==============================================================================

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
