# coding: utf-8
import datetime
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
  user_reviews = Review.objects.filter(user__id=user.id)
  context = RequestContext(request, {'user_reviews': user_reviews, 'page_user': user})
  return render_to_response('reviews/reviews.html', context)

@login_required
def new(request):
  if request.method == 'POST':
    short_name = request.POST['short-name']
    title = request.POST['title']
    description = request.POST['description']
    user = request.user
    last_update = datetime.date.today()
    review = Review(short_name = short_name, title = title, description = description, user=user, last_update=last_update)
    review.save()
    messages.add_message(request, messages.SUCCESS, 'Review created with success.')
    return redirect('/' + request.user.username + '/')
  else:
    context = RequestContext(request)
    return render_to_response('reviews/new.html', context)

@login_required
def review(request, username, review_name):
  review = Review.objects.get(short_name=review_name)
  context = RequestContext(request, {'review': review})
  return render_to_response('reviews/review.html', context)