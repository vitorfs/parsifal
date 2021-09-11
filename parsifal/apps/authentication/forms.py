from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.utils.translation import gettext

from parsifal.apps.authentication.validators import (
    ASCIIUsernameValidator,
    validate_case_insensitive_email,
    validate_case_insensitive_username,
    validate_forbidden_usernames,
)
from parsifal.apps.invites.constants import InviteStatus
from parsifal.apps.invites.models import Invite
from parsifal.utils.recaptcha import recaptcha_is_valid


class ASCIIUsernameField(UsernameField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(ASCIIUsernameValidator())
        self.validators.append(validate_forbidden_usernames)
        self.validators.append(validate_case_insensitive_username)


class SignUpForm(UserCreationForm):
    invite = forms.ModelChoiceField(
        queryset=Invite.objects.filter(invitee=None, status=InviteStatus.PENDING),
        required=False,
        widget=forms.HiddenInput(),
    )

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")
        field_classes = {"username": ASCIIUsernameField}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = gettext("Required. 150 characters or fewer. Letters, digits and . _ only.")
        self.fields["email"].validators.append(validate_case_insensitive_email)
        self.fields["email"].required = True

    def clean(self):
        cleaned_data = super().clean()
        if self.request and not recaptcha_is_valid(self.request):
            self.add_error(None, gettext("The Google reCAPTCHA did not validate. Please try again."))
        return cleaned_data

    def accept_invite(self, user):
        invite = self.cleaned_data.get("invite")
        if invite:
            invite.accept(user)
        # check if there are currently any invitation with this user email
        # and associate with their account
        Invite.objects.filter(invitee=None, status=InviteStatus.PENDING, invitee_email__iexact=user.email).update(
            invitee=user
        )

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            self.accept_invite(user)
        return user
