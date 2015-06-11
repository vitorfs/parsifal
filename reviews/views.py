# coding: utf-8

from django.core.urlresolvers import reverse as r
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect, get_object_or_404, render
from django.template import RequestContext
from django.utils.html import escape

from parsifal.decorators import ajax_required
from reviews.models import Review
from reviews.decorators import main_author_required, author_required
from reviews.forms import CreateReviewForm, ReviewForm


def reviews(request, username):
    user = get_object_or_404(User, username__iexact=username)
    followers = user.profile.get_followers()
    is_following = False
    if request.user in followers:
        is_following = True

    followers_count = user.profile.get_followers_count()
    following_count = user.profile.get_following_count()

    user_reviews = user.profile.get_reviews()

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
    if request.method == 'POST':
        form = CreateReviewForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user

            name = slugify(form.instance.title)
            unique_name = name
            i = 0
            while Review.objects.filter(name=unique_name, author__username=request.user.username):
                i = i + 1
                unique_name = u'{0}-{1}'.format(name, i)
            form.instance.name = unique_name
            review = form.save()
            messages.success(request, u'Review created successfully.')
            return redirect(r('review', args=(review.author.username, review.name)))
    else:
        form = CreateReviewForm()
    return render(request, 'reviews/new.html', { 'form': form })



@login_required
def review(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username__iexact=username)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            name = slugify(form.instance.name)
            unique_name = name
            if unique_name != review_name:
                i = 0
                while Review.objects.filter(name=unique_name, author__username=review.author.username):
                    i = i + 1
                    unique_name = u'{0}-{1}'.format(name, i)
            form.instance.name = unique_name
            review = form.save()
            messages.success(request, u'Review was saved successfully.')
            return redirect(r('review', args=(review.author.username, review.name)))
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/review.html', { 
            'review': review,
            'form': form
            })


@main_author_required
@login_required
def add_author_to_review(request):
    try:
        username = request.GET['username']
        review_id = request.GET['review-id']
        
        try:
            user = User.objects.get(username__iexact=username)
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
            return HttpResponse('Your review has been saved successfully!')
    except:
        return HttpResponseBadRequest()

@author_required
@login_required
def leave(request):
    review_id = request.POST.get('review-id')
    review = get_object_or_404(Review, pk=review_id)
    review.co_authors.remove(request.user)
    review.save()
    messages.add_message(request, messages.SUCCESS, u'You successfully left the review {0}.'.format(review.title))
    return redirect('/' + request.user.username + '/')
