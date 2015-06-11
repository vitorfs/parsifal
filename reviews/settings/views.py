# coding: utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from reviews.models import Review
from reviews.decorators import main_author_required
from parsifal.decorators import ajax_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.contrib.auth.models import User

@main_author_required
@login_required
def settings(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username=username)
    context = RequestContext(request, {'review': review,})
    return render_to_response('settings/review_settings.html', context)


@main_author_required
@login_required
def save_settings(request):
    try:
        review_id = request.POST['review-id']
        name = request.POST['name']
        title = request.POST['title']
        unique_name = slugify(name[:250])
        review = Review.objects.get(pk=review_id)

        if name and title:
            if unique_name != review.name:
                i = 0
                while Review.objects.filter(name=unique_name, author__username=review.author.username):
                    i = i + 1
                    unique_name = name + '-' + str(i)
            review.name = unique_name
            review.title = title[:250]
            review.save()
            messages.add_message(request, messages.SUCCESS, 'Review settings saved with success.')
            return HttpResponse('/' + review.author.username + '/' + review.name + '/settings/')
        else:
            messages.add_message(request, messages.ERROR, 'Name and Title are required fields.')
            return HttpResponse('/' + review.author.username + '/' + review.name + '/settings/')
    except Exception, e:
        return HttpResponseBadRequest()


@main_author_required
@login_required
def transfer(request):
    try:
        review_id = request.POST['review-id']
        transfer_user_username = request.POST['transfer-user']
        review = Review.objects.get(pk=review_id)
        try:
            transfer_user = User.objects.get(username=transfer_user_username)
        except Exception, e:
            return HttpResponseBadRequest('User not found.')
        current_user = request.user
        if current_user != transfer_user:
            if transfer_user in review.co_authors.all():
                review.co_authors.remove(transfer_user)
            review.author = transfer_user
            review.co_authors.add(current_user)
            review.save()
            return HttpResponse('/' + review.author.username + '/' + review.name + '/')
        else:
            return HttpResponseBadRequest('Hey! You can\'t transfer the review to yourself.')
    except Exception, e:
        return HttpResponseBadRequest('Something went wrong.')


@main_author_required
@login_required
def delete(request):
    try:
        review_id = request.POST['review-id']
        review = Review.objects.get(pk=review_id)
        username = review.author.username

        sources = review.sources.all()
        
        for source in sources:
            if not source.is_default:
                review.sources.remove(source)
                source.delete()

        review.delete()
        messages.add_message(request, messages.SUCCESS, 'The review was deleted successfully.')
        return HttpResponse('/' + username + '/')
    except Exception, e:
        return HttpResponseBadRequest('Something went wrong.')