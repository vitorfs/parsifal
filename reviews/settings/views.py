# coding: utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from reviews.models import Review

@login_required
def settings(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username=username)
    context = RequestContext(request, {'review': review,})
    return render_to_response('settings/review_settings.html', context)

@login_required
def save_settings(request, username, review_name):
    context = RequestContext(request)
    return render_to_response('settings/review_settings.html', context)