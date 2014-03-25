# coding: utf-8
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from reviews.models import *
from reviews.decorators import author_required

@author_required
@login_required
def reporting(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username=username)
    context = RequestContext(request, {'review': review})
    return render_to_response('reporting/reporting.html', context)

def articles_selection_chart(request):
    review_id = request.GET['review-id']
    review = Review.objects.get(pk=review_id)
    articles_selection = []
    for source in review.sources.all():
        count = review.get_source_articles(source.id).count()
        articles_selection.append(source.name + ':' + str(count))
    str_return = ','.join(articles_selection)
    return HttpResponse(str_return)
