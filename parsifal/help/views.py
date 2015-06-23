# coding: utf-8

from django.shortcuts import render, get_object_or_404

from parsifal.help.models import Article, Category


def articles(request):
    articles = Article.objects.filter(is_active=True).order_by('views',)
    return render(request, 'help/articles.html', { 'articles': articles })

def article(request, slug):
    article = get_object_or_404(Article, slug=slug, is_active=True)
    return render(request, 'help/article.html', { 'article': article })
