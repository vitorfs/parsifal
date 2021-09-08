import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from parsifal.apps.invites.constants import InviteStatus
from parsifal.apps.reviews.models import Review


class Invite(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, verbose_name=_("review"), related_name="invites")
    invited_by = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("invited by"), related_name="invites_sent"
    )
    invitee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("invitee"),
        related_name="invites_received",
    )
    invitee_email = models.EmailField(_("invitee email"), db_index=True)
    status = models.CharField(_("status"), max_length=32, choices=InviteStatus.CHOICES, default=InviteStatus.PENDING)
    code = models.UUIDField(_("code"), default=uuid.uuid4, editable=False)
    date_sent = models.DateTimeField(_("date sent"), auto_now_add=True)
    date_answered = models.DateTimeField(_("date answered"), null=True, blank=True)

    class Meta:
        verbose_name = _("invite")
        verbose_name_plural = _("invites")

    def __str__(self):
        return f"{self.review.name} - {self.get_invitee_email()} - {self.get_status_display()}"

    def get_invitee_email(self):
        if self.invitee:
            return self.invitee.email
        return self.invitee_email

    def accept(self):
        self.status = InviteStatus.ACCEPTED
        self.date_answered = timezone.now()

    def reject(self):
        self.status = InviteStatus.REJECTED
        self.date_answered = timezone.now()
