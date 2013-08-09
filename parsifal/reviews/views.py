# coding: utf-8
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from reviews.models import Review

@login_required
def reviews(request, username):
  context = RequestContext(request)
  user = get_object_or_404(User, username=username)
  user_reviews = Review.objects.all()
  context = RequestContext(request, {'user_reviews': user_reviews,})
  return render_to_response('reviews/reviews.html', context)

@login_required
def new(request):
  if request.method == 'POST':
    short_name = request.POST['short-name']
    title = request.POST['title']
    description = request.POST['description']
    review = Review(short_name = short_name, title = title, description = description)
    review.save()
    messages.add_message(request, messages.SUCCESS, 'Review created with success.')
    return redirect('/admin/')
  else:
    context = RequestContext(request)
    return render_to_response('reviews/new.html', context)

@login_required
def review(request):
  context = RequestContext(request)
  return render_to_response('reviews/review.html', context)