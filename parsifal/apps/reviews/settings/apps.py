from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SettingsConfig(AppConfig):
    name = "parsifal.apps.reviews.settings"
    verbose_name = _("Reviews: Settings")
