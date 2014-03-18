from django import forms
from reviews.models import Article, Review

class ArticleForm(forms.ModelForm):
    review = forms.ModelChoiceField(queryset=Review.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Article
        exclude = ['review', 'source', 'search_session']