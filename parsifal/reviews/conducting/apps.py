from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ConductingConfig(AppConfig):
    name = "parsifal.reviews.conducting"
    verbose_name = _("Reviews: Conducting")
