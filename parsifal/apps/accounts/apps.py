from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountSettingsConfig(AppConfig):
    name = "parsifal.apps.accounts"
    verbose_name = _("Account Settings")
