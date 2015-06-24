from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from reviews.models import Review, Article


def index(request):
    reviews = Review.objects.filter(author=request.user)
    document_list = Article.objects.filter(review__author=request.user)
    paginator = Paginator(document_list, 25)
    page = request.GET.get('page')
    try:
        documents = paginator.page(page)
    except PageNotAnInteger:
        documents = paginator.page(1)
    except EmptyPage:
        documents = paginator.page(paginator.num_pages)
    return render(request, 'library/library.html', { 'reviews': reviews, 'documents': documents })

