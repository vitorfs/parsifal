# coding: utf-8
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

@login_required
def reviews(request, username):
    context = RequestContext(request)
    return render_to_response('reviews/reviews.html', context)

@login_required
def new(request):
    context = RequestContext(request)
    return render_to_response('reviews/new.html', context)

@login_required
def review(request):
    context = RequestContext(request)
    return render_to_response('reviews/review.html', context)