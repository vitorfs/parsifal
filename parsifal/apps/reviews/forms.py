from django import forms
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from parsifal.apps.reviews.models import Review


class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = (
            "title",
            "description",
        )
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": _("Systematic literature review's title")}),
            "description": forms.Textarea(
                attrs={"placeholder": _("Give a brief description of your systematic literature review")}
            ),
        }

    def __init__(self, *args, request, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        self.fields["description"].help_text = _("Try to keep it short, max 500 characters :)")

    def save(self, commit=True):
        self.instance = super().save(commit=False)
        self.instance.author = self.request.user
        name = slugify(self.cleaned_data.get("title"))
        if not name:
            name = "literature-review"
        unique_name = name
        i = 0
        while Review.objects.filter(name=unique_name, author=self.request.user).exists():
            i += 1
            unique_name = f"{name}-{i}"
        self.instance.name = unique_name
        if commit:
            self.instance.save()
        return self.instance


class UpdateReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = (
            "title",
            "description",
        )
        widgets = {"description": forms.Textarea(attrs={"class": "expanding", "rows": "4"})}
