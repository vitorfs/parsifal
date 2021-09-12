from django import forms
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.utils.translation import gettext as _

from parsifal.apps.invites.constants import InviteStatus
from parsifal.apps.invites.models import Invite


class SendInviteForm(forms.ModelForm):
    class Meta:
        model = Invite
        fields = ("invitee", "invitee_email")

    def __init__(self, *args, request, review, **kwargs):
        self.request = request
        self.review = review
        super().__init__(*args, **kwargs)
        user_ids = {user.pk for user in self.request.user.profile.get_following()}
        self.fields["invitee"].queryset = (
            User.objects.filter(pk__in=user_ids)
            .exclude(pk__in=self.review.co_authors.all())
            .annotate(lower_username=Lower("username"))
            .order_by("lower_username")
        )
        self.fields["invitee"].label = _("Contacts")
        self.fields["invitee"].help_text = _("List of people that you are currently following on Parsifal.")

        self.fields["invitee_email"].label = _("Email address of the person you want to invite")
        self.fields["invitee_email"].help_text = _(
            "If the person you want to invite is not on Parsifal, you can inform their email address and we will send "
            "an invitation link to their inbox."
        )
        self.fields["invitee_email"].required = False

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("invitee") and cleaned_data.get("invitee_email"):
            self.add_error(
                None, _("You must inform either a contact or an email address, but not both at the same time.")
            )
        if not cleaned_data.get("invitee") and not cleaned_data.get("invitee_email"):
            self.add_error(None, _("You must inform either a contact or an email address."))
        return cleaned_data

    def clean_invitee(self):
        invitee = self.cleaned_data.get("invitee")
        if invitee:
            if self.review.is_author_or_coauthor(invitee):
                self.add_error("invitee", _("This person is already a co-author of this review."))
            if Invite.objects.filter(
                review=self.review, invitee_email__iexact=invitee.email, status=InviteStatus.PENDING
            ).exists():
                self.add_error("invitee", _("This person already has a pending invite."))
        return invitee

    def clean_invitee_email(self):
        invitee_email = self.cleaned_data.get("invitee_email")
        if invitee_email:
            invitee_email = User.objects.normalize_email(invitee_email)
            if invitee_email.lower() == self.request.user.email.lower():
                self.add_error("invitee_email", _("You cannot invite yourself."))
            try:
                user = User.objects.get(email__iexact=invitee_email)
                if self.review.is_author_or_coauthor(user):
                    self.add_error("invitee_email", _("This person is already a co-author of this review."))
            except User.DoesNotExist:
                pass
            if Invite.objects.filter(
                review=self.review, invitee_email__iexact=invitee_email, status=InviteStatus.PENDING
            ).exists():
                self.add_error("invitee_email", _("This person already has a pending invite."))
        return invitee_email

    def save(self, commit=True):
        self.instance = super().save(commit=False)
        if self.instance.invitee:
            self.instance.invitee_email = self.instance.invitee.email
        else:
            self.instance.invitee = User.objects.filter(email__iexact=self.instance.invitee_email).first()
        self.instance.review = self.review
        self.instance.invited_by = self.request.user
        if commit:
            self.instance.save()
        return self.instance
