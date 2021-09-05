from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HelpConfig(AppConfig):
    name = "parsifal.apps.help"
    verbose_name = _("Help")
