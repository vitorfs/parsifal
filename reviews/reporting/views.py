# coding: utf-8
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from reviews.models import *
from reviews.decorators import author_required
from django.db.models import Count

@author_required
@login_required
def reporting(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username=username)
    context = RequestContext(request, {'review': review})
    return render_to_response('reporting/reporting.html', context)

def articles_selection_chart(request):
    review_id = request.GET['review-id']
    review = Review.objects.get(pk=review_id)
    selected_articles = review.get_accepted_articles()
    articles = []
    for source in review.sources.all():
        count = review.get_source_articles(source.id).count()
        accepted_count = selected_articles.filter(source__id=source.id).count()
        articles.append(source.name + ':' + str(count) + ':' + str(accepted_count))
    return HttpResponse(','.join(articles))

def articles_per_year(request):
    review_id = request.GET['review-id']
    review = Review.objects.get(pk=review_id)
    final_articles = review.get_final_selection_articles().values('year').annotate(count=Count('year')).order_by('-year')
    articles = []
    for article in final_articles:
        articles.append(article['year'] + ':' + str(article['count']))
    return HttpResponse(','.join(articles))