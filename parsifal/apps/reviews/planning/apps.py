from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PlanningConfig(AppConfig):
    name = "parsifal.apps.reviews.planning"
    verbose_name = _("Reviews: Planning")
