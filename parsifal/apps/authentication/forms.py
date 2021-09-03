from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.utils.translation import gettext

from parsifal.apps.authentication.validators import (
    ASCIIUsernameValidator,
    validate_case_insensitive_email,
    validate_case_insensitive_username,
    validate_forbidden_usernames,
)


class ASCIIUsernameField(UsernameField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(ASCIIUsernameValidator())
        self.validators.append(validate_forbidden_usernames)
        self.validators.append(validate_case_insensitive_username)


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")
        field_classes = {"username": ASCIIUsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = gettext("Required. 150 characters or fewer. Letters, digits and . _ only.")
        self.fields["email"].validators.append(validate_case_insensitive_email)
        self.fields["email"].required = True
