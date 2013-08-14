# coding: utf-8
import datetime
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.utils.html import escape
from reviews.models import Review, Source, ReferenceArticle
from pybtex.database.input import bibtex

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
    parser = bibtex.Parser()
    bibdata = parser.parse_file("/Users/vitorfs/Downloads/scopus.bib")

    articles = []
    for bib_id in bibdata.entries:
        b = bibdata.entries[bib_id].fields
        article = ReferenceArticle()

        try:
            article.title = b["title"]
            article.journal = b["journal"]
            article.year = b["year"]
            article.author = b["author"]
            article.id = bib_id
        except(KeyError):
            continue

        articles.append(article)

    review = Review.objects.get(short_name=review_name)
    context = RequestContext(request, {'review': review, 'articles': articles})
    return render_to_response('reviews/conducting.html', context)

@login_required
def add_source_to_review(request):
    '''
        Function used via Ajax request only.
        This function adds a new source to the source list of the review.
        To add the source successfully the logged in user must be the author or a co-author
        of the review.
    '''
    review_id = request.GET['id']
    name = request.GET['name']
    url = request.GET['url']
    source = Source(name=name, url=url)
    source.save()

    review = Review.objects.get(pk=review_id)
    if review.user.id == request.user.id:
        review.sources.add(source)
        review.save()
        return_html = '<tr source-id="' + str(source.id) + '"><td>' + escape(source.name) + '</td><td>' + escape(source.url) + '</td><td><button type="button" class="btn btn-small">edit</button> <button type="button" class="btn btn-warning btn-small btn-remove-source">remove</a></td></tr>'
        return HttpResponse(return_html)
    else:
        return HttpResponse('error')

@login_required
def remove_source_from_review(request):
    '''
        Function used via Ajax request only.
    '''
    source_id = request.GET['source_id']
    review_id = request.GET['review_id']
    source = Source.objects.get(pk=source_id)
    review = Review.objects.get(pk=review_id)
    review.sources.remove(source)
    source.delete()
    review.save()
    return HttpResponse('OK')