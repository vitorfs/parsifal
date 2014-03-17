from django import forms
from reviews.models import Article

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        exclude = ['review', 'source', 'search_session']