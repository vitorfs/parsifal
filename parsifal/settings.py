from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
from unipath import Path
import dj_database_url
from decouple import config
from mendeley import Mendeley

#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)

PROJECT_DIR = Path(__file__).parent

DEBUG = config('DEBUG', default=False, cast=bool) 
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': dj_database_url.config(
      default = config('DATABASE_URL'))
}

ALLOWED_HOSTS = ['127.0.0.1', '162.243.206.171', 'parsif.al']

ADMINS = (
    ('Vitor Freitas', 'vitorfs@gmail.com'),
)

MANAGERS = ADMINS

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = PROJECT_DIR.parent.parent.child('media')
MEDIA_URL = '/media/'
FILE_UPLOAD_TEMP_DIR = '/tmp/'
FILE_UPLOAD_PERMISSIONS = 0644
FILE_UPLOAD_MAX_MEMORY_SIZE = 33554432

STATIC_ROOT = PROJECT_DIR.parent.parent.child('static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    PROJECT_DIR.child('static'),
)

SECRET_KEY = config('SECRET_KEY')

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'parsifal.urls'

WSGI_APPLICATION = 'parsifal.wsgi.application'

TEMPLATE_DIRS = (
    PROJECT_DIR.child('templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'reviews',
    'reviews.planning',
    'reviews.conducting',
    'reviews.reporting',
    'reviews.settings',
    'reviews.publish',
    'parsifal.account_settings',
    'parsifal.activities',
    'parsifal.authentication',
    'parsifal.blog',
    'parsifal.core',
    'parsifal.help',
    'parsifal.library',
)

LOGIN_URL = '/signin/'
LOGOUT_URL = '/signout/'

EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_FILE_PATH = PROJECT_DIR.parent.child('maildumps')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
DEFAULT_FROM_EMAIL = 'Parsifal Team <noreply@parsif.al>'
EMAIL_SUBJECT_PREFIX = '[Parsifal] '
SERVER_EMAIL = 'application@parsif.al'

MENDELEY_ID = config('MENDELEY_ID', cast=int)
MENDELEY_SECRET = config('MENDELEY_SECRET')
MENDELEY_REDIRECT_URI = config('MENDELEY_REDIRECT_URI')
MENDELEY = Mendeley(MENDELEY_ID, client_secret=MENDELEY_SECRET, redirect_uri=MENDELEY_REDIRECT_URI)

DROPBOX_APP_KEY = config('DROPBOX_APP_KEY')
DROPBOX_SECRET = config('DROPBOX_SECRET')
DROPBOX_REDIRECT_URI = config('DROPBOX_REDIRECT_URI')

ELSEVIER_API_KEY = config('ELSEVIER_API_KEY')

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: '/%s/' % u.username,
}
