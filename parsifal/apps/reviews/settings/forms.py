from django import forms
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from parsifal.apps.reviews.models import Review


class ReviewSettingsForm(forms.ModelForm):
    author = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=User.objects.all(), disabled=True)

    class Meta:
        model = Review
        fields = (
            "author",
            "name",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = _("URL")
        current_url = format_html(
            "/{username}/<strong>{review_name}</strong>/",
            username=self.instance.author.username,
            review_name=self.instance.name,
        )
        self.fields["name"].help_text = (
            _("Only letters, numbers, underscores or hyphens are allowed.<br>The current URL of your review is %s")
            % current_url
        )
