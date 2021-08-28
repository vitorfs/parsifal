from pathlib import Path

from django.utils.translation import gettext_lazy as _

import dj_database_url
from decouple import Csv, config

# ==============================================================================
# CORE SETTINGS
# ==============================================================================

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

SECRET_KEY = config("SECRET_KEY", default="parsifal.settings.local")

DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost", cast=Csv())

ADMINS = (("Vitor Freitas", "vitorfs@gmail.com"),)

MANAGERS = ADMINS

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.contrib.humanize",
    "parsifal.reviews",
    "parsifal.reviews.planning",
    "parsifal.reviews.conducting",
    "parsifal.reviews.reporting",
    "parsifal.reviews.settings",
    "parsifal.account_settings",
    "parsifal.activities",
    "parsifal.authentication",
    "parsifal.blog",
    "parsifal.core",
    "parsifal.help",
    "parsifal.library",
)

INTERNAL_IPS = ["127.0.0.1"]

ROOT_URLCONF = "parsifal.urls"

WSGI_APPLICATION = "parsifal.wsgi.application"

SITE_ID = 1

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ==============================================================================
# MIDDLEWARE SETTINGS
# ==============================================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
]


# ==============================================================================
# TEMPLATES SETTINGS
# ==============================================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ==============================================================================
# DATABASES SETTINGS
# ==============================================================================

DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL", default="postgres://richardwagner:holygrail@localhost:5432/parsifal"),
        conn_max_age=600,
    )
}

# ==============================================================================
# AUTHENTICATION AND AUTHORIZATION SETTINGS
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda u: "/%s/" % u.username,
}

LOGIN_URL = "/signin/"
LOGOUT_URL = "/signout/"


# ==============================================================================
# INTERNATIONALIZATION AND LOCALIZATION SETTINGS
# ==============================================================================

LANGUAGE_CODE = config("LANGUAGE_CODE", default="en-us")

TIME_ZONE = config("TIME_ZONE", default="UTC")

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (("en-us", _("English")), ("pt-br", _("Brazilian Portuguese")))

LOCALE_PATHS = [str(BASE_DIR / "locale")]


# ==============================================================================
# STATIC FILES SETTINGS
# ==============================================================================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR.parent.parent / "static"
STATICFILES_DIRS = [str(BASE_DIR / "static")]
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)


# ==============================================================================
# MEDIA FILES SETTINGS
# ==============================================================================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR.parent.parent / "media/"
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"


# ==============================================================================
# THIRD-PARTY APPS
# ==============================================================================

ELSEVIER_API_KEY = config("ELSEVIER_API_KEY")
