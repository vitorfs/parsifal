# flake8: noqa

from .base import *

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]


class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()
