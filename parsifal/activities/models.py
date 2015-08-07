from django.db import models
from django.contrib.auth.models import User

from parsifal.reviews.models import Review


class Activity(models.Model):
    FOLLOW = 'F'
    COMMENT = 'C'
    STAR = 'S'
    ACTIVITY_TYPES = (
        (FOLLOW, 'Follow'),
        (COMMENT, 'Comment'),
        (STAR, 'Star'),
    )

    from_user = models.ForeignKey(User)
    to_user = models.ForeignKey(User, related_name="+", null=True)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    content = models.CharField(max_length=500, blank=True)
    review = models.ForeignKey(Review, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"

    def __unicode__(self):
        return self.activity_type
