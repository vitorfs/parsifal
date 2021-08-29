from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render

from parsifal.help.models import Article


def articles(request):
    articles = (
        Article.objects.select_related("category")
        .filter(is_active=True)
        .order_by(
            "category__name",
            "title",
        )
    )
    return render(request, "help/articles.html", {"articles": articles})


def article(request, slug):
    article = get_object_or_404(Article, slug=slug, is_active=True)
    Article.objects.filter(pk=article.pk).update(views=F("views") + 1)
    return render(request, "help/article.html", {"article": article})


def search(request):
    if "q" in request.GET:
        querystring = request.GET.get("q").strip()
        if querystring:
            articles = (
                Article.objects.filter(is_active=True)
                .filter(Q(title__icontains=querystring) | Q(content__icontains=querystring))
                .order_by("title")
            )
            return render(request, "help/search.html", {"articles": articles, "querystring": querystring})
    return redirect("help:articles")
