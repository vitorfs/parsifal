# coding: utf-8

from django.core.urlresolvers import reverse as r
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from parsifal.help.models import Article


def articles(request):
    articles = Article.objects.filter(is_active=True).order_by('category__name', 'title',)
    return render(request, 'help/articles.html', { 'articles': articles })

def article(request, slug):
    article = get_object_or_404(Article, slug=slug, is_active=True)
    article.views += 1
    article.save()
    return render(request, 'help/article.html', { 'article': article })

def search(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        if querystring:
            articles = Article.objects \
                    .filter(is_active=True) \
                    .filter(Q(title__icontains=querystring) | Q(content__icontains=querystring)) \
                    .order_by('title')
            return render(request, 'help/search.html', { 'articles': articles, 'querystring': querystring })
    return redirect(r('help:articles'))