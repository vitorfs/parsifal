from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ActivitiesConfig(AppConfig):
    name = "parsifal.apps.activities"
    verbose_name = _("Activities")
