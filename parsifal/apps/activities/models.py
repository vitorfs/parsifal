from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from parsifal.apps.activities.constants import ActivityTypes
from parsifal.apps.reviews.models import Review


class Activity(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("from user"))
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+", null=True, verbose_name=_("to user"))
    activity_type = models.CharField(_("type"), max_length=1, choices=ActivityTypes.CHOICES)
    content = models.CharField(_("content"), max_length=500, blank=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True, verbose_name=_("review"))
    date = models.DateTimeField(_("date"), auto_now_add=True)

    class Meta:
        verbose_name = _("activity")
        verbose_name_plural = _("activities")

    def __str__(self):
        return self.get_activity_type_display()
