from django.shortcuts import render

from reviews.models import Article


def index(request):
    documents = Article.objects.all()[:20]
    return render(request, 'library/library.html', { 'documents': documents })
