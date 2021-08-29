from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BlogConfig(AppConfig):
    name = "parsifal.apps.blog"
    verbose_name = _("Blog")
