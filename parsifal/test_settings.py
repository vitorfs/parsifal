from settings import *

DATABASES['default'] = { 'ENGINE': 'django.db.backends.sqlite3' }

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

class DisableMigrations(object):
    def __contains__(self, item):
        return True
    def __getitem__(self, item):
        return 'notmigrations'

MIGRATION_MODULES = DisableMigrations()
