# coding: utf-8
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.utils.html import escape
from reviews.models import Review
from reviews.decorators import main_author_required, author_required
from parsifal.decorators import ajax_required
from utils.viewhelper import Table
from django.template.defaultfilters import slugify

def reviews(request, username):
    user = get_object_or_404(User, username=username)
    followers = user.profile.get_followers()
    is_following = False
    if request.user in followers:
        is_following = True

    followers_count = user.profile.get_followers_count()
    following_count = user.profile.get_following_count()

    user_reviews = Review.objects.filter(author__id=user.id).order_by('-last_update',)
    context = RequestContext(request, {
        'user_reviews': user_reviews, 
        'page_user': user, 
        'is_following': is_following,
        'following_count': following_count,
        'followers_count': followers_count
        })
    return render_to_response('reviews/reviews.html', context)

@login_required
def new(request):
    review = Review()
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        author = request.user

        name = slugify(title)
        unique_name = name
        i = 0

        while Review.objects.filter(name=unique_name, author__username=request.user.username):
            i = i + 1
            unique_name = name + '-' + str(i)

        review = Review(name = unique_name, title = title, description = description, author=author)
        if title:
            review.save()
            messages.add_message(request, messages.SUCCESS, 'Review created with success.')
            return redirect('/' + review.author.username + '/' + review.name + '/')
        else:
            message = 'Title is a required field.'
            messages.add_message(request, messages.ERROR, message)
    context = RequestContext(request, {'review': review})
    return render_to_response('reviews/new.html', context)

@login_required
def review(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username=username)
    context = RequestContext(request, {'review': review})
    return render_to_response('reviews/review.html', context)

@ajax_required
@main_author_required
@login_required
def add_author_to_review(request):
    try:
        username = request.GET['username']
        review_id = request.GET['review-id']
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        review = Review.objects.get(pk=review_id)

        if user is not None and user.id != review.author.id:
            review.co_authors.add(user)
            review.save()
            return HttpResponse('<li author-id="' + str(user.id) + '"><a href="/' + user.username +'/">' + user.profile.get_screen_name() + '</a> <button type="button" class="btn btn-small btn-link remove-author text-error">(remove)</button></li>')
        else:
            return HttpResponseBadRequest()
    except:
        return HttpResponseBadRequest()

@ajax_required
@main_author_required
@login_required
def remove_author_from_review(request):
    try:
        author_id = request.GET['author-id']
        review_id = request.GET['review-id']
        author = User.objects.get(pk=author_id)
        review = Review.objects.get(pk=review_id)
        review.co_authors.remove(author)
        review.save()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def save_description(request):
    try:
        review_id = request.POST['review-id']
        description = request.POST['description']
        review = Review.objects.get(pk=review_id)
        if len(description) > 500:
            return HttpResponseBadRequest('The review description should not exceed 500 characters. The given description have %s characters.' % len(description))
        else:
            review.description = description
            review.save()
            return HttpResponse('Your review have been saved successfully!')
    except:
        return HttpResponseBadRequest()