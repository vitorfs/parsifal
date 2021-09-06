from django.utils.translation import gettext_lazy as _


class ActivityTypes:
    FOLLOW = "F"
    COMMENT = "C"
    STAR = "S"

    CHOICES = (
        (FOLLOW, _("Follow")),
        (COMMENT, _("Comment")),
        (STAR, _("Star")),
    )
