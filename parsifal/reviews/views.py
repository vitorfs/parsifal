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
  user_reviews = Review.objects.filter(user__id=user.id).order_by('-last_update',)
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

@login_required
def add_author_to_review(request):
  username = request.GET['username']
  review_id = request.GET['id']
  
  try:
    user = User.objects.get(username=username)
  except User.DoesNotExist:
    user = None

  if user is not None:
    review = Review.objects.get(pk=review_id)
    if review.user.id == request.user.id:
      review.co_authors.add(user)
      review.save()
      return HttpResponse('<li author-id="' + str(user.id) + '"><a href="/' + user.username +'/">' + user.get_full_name() + '</a> <button type="button" class="remove-author">(remove)</button></li>')
    else:
      return HttpResponse('error')
  else:
    return HttpResponse('error')

@login_required
def remove_author_from_review(request):
  author_id = request.GET['author_id']
  review_id = request.GET['review_id']
  author = User.objects.get(pk=author_id)
  review = Review.objects.get(pk=review_id)
  review.co_authors.remove(author)
  review.save()
  return HttpResponse('OK')

@login_required
def planning(request, username, review_name):
  review = Review.objects.get(short_name=review_name)
  context = RequestContext(request, {'review': review})
  return render_to_response('reviews/planning.html', context)

@login_required
def conducting(request, username, review_name):
  review = Review.objects.get(short_name=review_name)
  context = RequestContext(request, {'review': review})
  return render_to_response('reviews/conducting.html', context)