from django import forms

from parsifal.apps.reviews.models import Review


class CreateReviewForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Systematic literature review's title"}),
        max_length=2550,
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Give a brief description of your systematic literature review",
            }
        ),
        max_length=5000,
        help_text="Try to keep it short, max 500 characters :)",
        required=False,
    )

    class Meta:
        model = Review
        fields = [
            "title",
            "description",
        ]


class ReviewForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), max_length=2550)
    description = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control expanding", "rows": "4"}), max_length=5000, required=False
    )

    class Meta:
        model = Review
        fields = [
            "title",
            "description",
        ]
