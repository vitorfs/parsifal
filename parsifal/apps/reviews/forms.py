from django import forms
from django.utils.translation import gettext_lazy as _

from parsifal.apps.reviews.models import Review


class CreateReviewForm(forms.ModelForm):
    title = forms.CharField(
        label=_("Title"),
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Systematic literature review's title")}
        ),
        max_length=255,
    )
    description = forms.CharField(
        label=_("Description"),
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": _("Give a brief description of your systematic literature review"),
            }
        ),
        max_length=500,
        help_text=_("Try to keep it short, max 500 characters :)"),
        required=False,
    )

    class Meta:
        model = Review
        fields = (
            "title",
            "description",
        )


class ReviewForm(forms.ModelForm):
    title = forms.CharField(label=_("Title"), widget=forms.TextInput(attrs={"class": "form-control"}), max_length=255)
    description = forms.CharField(
        label=_("Description"),
        widget=forms.Textarea(attrs={"class": "form-control expanding", "rows": "4"}),
        max_length=500,
        required=False,
    )

    class Meta:
        model = Review
        fields = (
            "title",
            "description",
        )
