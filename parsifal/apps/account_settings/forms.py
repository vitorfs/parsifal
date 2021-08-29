from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), max_length=30, required=False
    )
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), max_length=30, required=False)
    public_email = forms.CharField(
        widget=forms.EmailInput(attrs={"class": "form-control"}), max_length=254, required=False
    )
    url = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), max_length=50, required=False)
    institution = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), max_length=50, required=False
    )
    location = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), max_length=50, required=False)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass

    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "public_email", "url", "institution", "location")

    def save(self, *args, **kwargs):
        u = self.instance.user
        u.first_name = self.cleaned_data["first_name"]
        u.last_name = self.cleaned_data["last_name"]
        u.save()
        profile = super().save(*args, **kwargs)
        return profile


class PasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"), widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    new_password1 = forms.CharField(
        label=_("New password"), widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    new_password2 = forms.CharField(
        label=_("Confirm password"), widget=forms.PasswordInput(attrs={"class": "form-control"})
    )