from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import gettext, gettext_lazy as _

from parsifal.apps.authentication.models import Profile


class UserEmailForm(forms.ModelForm):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        max_length=254,
        help_text=_(
            "This email account will not be publicly available. "
            "It is used for your Parsifal account management, "
            "such as internal notifications and password reset."
        ),
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email = User.objects.normalize_email(email)
        if User.objects.exclude(pk=self.instance.pk).filter(email__iexact=email).exists():
            raise ValidationError(gettext("User with this Email already exists."))
        return email


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label=_("First name"), max_length=150, required=False)
    last_name = forms.CharField(label=_("Last name"), max_length=150, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass

    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "public_email", "url", "institution", "location")

    @transaction.atomic()
    def save(self, commit=True):
        self.instance.user.first_name = self.cleaned_data["first_name"]
        self.instance.user.last_name = self.cleaned_data["last_name"]
        self.instance.user.save()
        return super().save(commit)
