from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from parsifal.apps.reviews.models import Review


class Activity(models.Model):
    FOLLOW = "F"
    COMMENT = "C"
    STAR = "S"
    ACTIVITY_TYPES = (
        (FOLLOW, _("Follow")),
        (COMMENT, _("Comment")),
        (STAR, _("Star")),
    )

    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+", null=True)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    content = models.CharField(max_length=500, blank=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("activity")
        verbose_name_plural = _("activities")

    def __str__(self):
        return self.get_activity_type_display()
