# coding: utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from reviews.models import Review
from reviews.decorators import author_required

@author_required
@login_required
def reporting(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username=username)
    context = RequestContext(request, {'review': review})
    return render_to_response('reporting/reporting.html', context)