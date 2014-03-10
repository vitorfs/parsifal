# coding: utf-8
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from reviews.models import Review, Source, Article, Question, Keyword
from reviews.decorators import main_author_required, author_required
from parsifal.decorators import ajax_required
from pybtex.database.input import bibtex
from django.conf import settings as django_settings
from utils.viewhelper import Table

@login_required
def conducting(request, username, review_name):
    return search_string(request, username, review_name)
    
@login_required
def search_string(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username=username)
    context = RequestContext(request, {'review': review})
    return render_to_response('conducting/conducting_search_string.html', context)

@login_required
def study_selection(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username=username)
    try:
        active_tab = int(request.GET['source'])
    except Exception, e:
        active_tab = -1

    context = RequestContext(request, {'review': review, 'active_tab': active_tab})
    return render_to_response('conducting/conducting_study_selection.html', context)

@login_required
def quality_assessment(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username=username)

    selected_studies = review.get_source_articles()
    quality_questions = review.get_quality_assessment_questions()
    quality_answers = review.get_quality_assessment_answers()    

    context = RequestContext(request, {'review': review, 
        'selected_studies': selected_studies,
        'quality_questions': quality_questions,
        'quality_answers': quality_answers,
    })
    return render_to_response('conducting/conducting_quality_assessment.html', context)

@login_required
def data_extraction(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username=username)
    context = RequestContext(request, {'review': review})
    return render_to_response('conducting/conducting_data_extraction.html', context)

def extract_keyword_to_search_string(term_list, query_list, keywords):
    for keyword in term_list:
        if keyword:
            query_list.append(keyword)
            synonyms = filter(lambda s: s.synonym_of is not None and s.synonym_of.description == keyword, keywords)
            for synonym in synonyms:
                if synonym:
                    query_list.append(synonym.description)
    return query_list

@ajax_required
@author_required
@login_required
def generate_search_string(request):
    '''
        Function used via Ajax request only.
        Still have to refactor this function. This is just a first approach.
    '''
    review_id = request.GET['review-id']
    review = Review.objects.get(pk=review_id)

    questions = Question.objects.filter(review__id=review_id)
    keywords = Keyword.objects.filter(review__id=review_id)

    population_list = []
    intervention_list = []
    comparison_list = []
    outcome_list = []

    query_population = []
    query_intervention = []
    query_comparison = []
    query_outcome = []

    for question in questions:
        population_list = question.population.split(',')
        intervention_list = question.intervention.split(',')
        comparison_list = question.comparison.split(',')
        outcome_list = question.outcome.split(',')

        query_population = extract_keyword_to_search_string(population_list, query_population, keywords)
        query_intervention = extract_keyword_to_search_string(intervention_list, query_intervention, keywords)
        query_comparison = extract_keyword_to_search_string(comparison_list, query_comparison, keywords)
        query_outcome = extract_keyword_to_search_string(outcome_list, query_outcome, keywords)

    str_population = ' OR '.join(query_population)
    str_intervention = ' OR '.join(query_intervention)
    str_comparison = ' OR '.join(query_comparison)
    str_outcome = ' OR '.join(query_outcome)

    search_string = []

    if str_population: search_string.append('(' + str_population + ')')
    if str_intervention: search_string.append('(' + str_intervention + ')')
    if str_comparison: search_string.append('(' + str_comparison + ')')
    if str_outcome: search_string.append('(' + str_outcome + ')')

    return HttpResponse(' AND '.join(search_string))

@ajax_required
@author_required
@login_required
def save_generic_search_string(request):
    try:
        review_id = request.POST['review-id']
        search_string = request.POST['search-string']
        review = Review.objects.get(pk=review_id)
        generic_search_string = review.get_generic_search_string()
        generic_search_string.search_string = search_string
        generic_search_string.save()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()

def bibtex_to_article_object(filename, review_id, source_id):
    parser = bibtex.Parser()
    bibdata = parser.parse_file(filename)
    articles = []
    for bib_id in bibdata.entries:
        b = bibdata.entries[bib_id].fields
        article = Article()
        try:
            article.title = b["title"]
            article.journal = b["journal"]
            article.year = b["year"]
            article.author = b["author"]
            article.abstract = b["abstract"]
            article.bibtex_key = bib_id
            article.review = Review(id=review_id)
            article.source = Source(id=source_id)
        except(KeyError):
            continue
        articles.append(article)
    return articles

@author_required
@login_required
def import_bibtex(request):
    review_id = request.POST['review-id']
    source_id = request.POST['source-id']
    review = Review.objects.get(pk=review_id)
    f = request.FILES['bibtex']
    filename = django_settings.MEDIA_ROOT + '/temp_bibitex_upload/' + request.user.username + '.bib'
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    articles = bibtex_to_article_object(filename, review_id, source_id)
    for article in articles:
        print article
        article.save()
    return redirect('/' + review.author.username + '/' + review.name + '/conducting/studies/?source=' + source_id)

@ajax_required
@author_required
@login_required
def source_articles(request):
    review_id = request.GET['review-id']
    source_id = request.GET['source-id']
    review = Review.objects.get(pk=review_id)
    articles = review.get_source_articles(source_id)
    if articles:
        html_table = Table()\
            .columns('bibtex_key', 'title', 'author', 'journal', 'year')\
            .data(articles)\
            .css_class('table')\
            .build()
        return HttpResponse(html_table)
    else:
        return HttpResponse("<h3>You haven't imported any article so far.</h3>")

@ajax_required
@author_required
@login_required
def article_details(request):
    article_id = request.GET['article-id']
    article = Article.objects.get(pk=article_id)
    status = Article.ARTICLE_STATUS
    context = RequestContext(request, {'article': article, 'status': status,})
    return render_to_response('conducting/partial_conducting_article_details.html', context)

@ajax_required
@author_required
@login_required
def save_article_details(request):
    try:
        article_id = request.POST['article-id']
        article = Article.objects.get(pk=article_id)
        status = request.POST['article-status']
        article.status = status
        article.save()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()