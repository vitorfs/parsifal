# coding: utf-8
import datetime
import time
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.utils.html import escape
from reviews.models import Review, Source, Article, Question, SelectionCriteria, Keyword
from reviews.decorators import main_author_required, author_required, ajax_required
from pybtex.database.input import bibtex

@login_required
def reviews(request, username):
    context = RequestContext(request)
    user = get_object_or_404(User, username=username)
    user_reviews = Review.objects.filter(author__id=user.id).order_by('-last_update',)
    context = RequestContext(request, {'user_reviews': user_reviews, 'page_user': user})
    return render_to_response('reviews/reviews.html', context)

@login_required
def new(request):
    if request.method == 'POST':
        name = request.POST['name']
        title = request.POST['title']
        description = request.POST['description']
        author = request.user
        last_update = datetime.date.today()
        review = Review(name = name, title = title, description = description, author=author, last_update=last_update)
        review.save()
        messages.add_message(request, messages.SUCCESS, 'Review created with success.')
        return redirect('/' + review.author.username + '/' + review.name + '/')
    else:
        context = RequestContext(request)
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
            return HttpResponse('<li author-id="' + str(user.id) + '"><a href="/' + user.username +'/">' + user.get_full_name() + '</a> <button type="button" class="btn btn-small btn-link remove-author text-error">(remove)</button></li>')
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

@login_required
def planning(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username=username)
    default_sources = Source.objects.filter(is_default=True)
    context = RequestContext(request, {'review': review, 'default_sources': default_sources })
    return render_to_response('reviews/planning.html', context)

@login_required
def conducting(request, username, review_name):
    parser = bibtex.Parser()
    bibdata = parser.parse_file("/Users/vitorfs/Downloads/scopus.bib")

    articles = []
    for bib_id in bibdata.entries:
        b = bibdata.entries[bib_id].fields
        article = Article()

        try:
            article.title = b["title"]
            article.journal = b["journal"]
            article.year = b["year"]
            article.author = b["author"]
            article.id = bib_id
        except(KeyError):
            continue

        articles.append(article)

    review = Review.objects.get(name=review_name, author__username=username)
    context = RequestContext(request, {'review': review, 'articles': articles})
    return render_to_response('reviews/conducting.html', context)

@login_required
def reporting(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username=username)
    context = RequestContext(request, {'review': review})
    return render_to_response('reviews/reporting.html', context)

def html_source(source):
    html = '<tr source-id="' + str(source.id) + '"><td>' + escape(source.name) + '</td>'
    if source.url:
        html += '<td><a href="' + escape(source.url) + '" target="_blank">' + escape(source.url) + '</a></td>'
    else:
        html += '<td>' + escape(source.url) + '</td>'
    html += '<td><button type="button" class="btn btn-small btn-edit-source">edit</button> <button type="button" class="btn btn-warning btn-small btn-remove-source">remove</a></td></tr>'
    return html

@ajax_required
@author_required
@login_required
def save_source(request):
    '''
        Function used via Ajax request only.
        This function adds a new source to the source list of the review.
        To add the source successfully the logged in user must be the author or a co-author
        of the review.
        If the request receives a source_id, that means the source already exist so the function
        will just edit the existing source and save the model.
    '''
    try:
        review_id = request.GET['review-id']
        source_id = request.GET['source-id']
        name = request.GET['name']
        url = request.GET['url']

        review = Review.objects.get(pk=review_id)
        if source_id:
            try:
                source = Source.objects.get(pk=source_id)
                if source.is_default:
                    review.sources.remove(source)
                    source = Source()
                source.name=name
                source.set_url(url)
                source.save()
            except Source.DoesNotExist:
                pass
        else:
            source = Source()
            source.name=name
            source.set_url(url)
            source.save()
            review.sources.add(source)
            review.save()
        return HttpResponse(html_source(source))
    except:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def remove_source_from_review(request):
    try:
        source_id = request.GET['source-id']
        review_id = request.GET['review-id']
        source = Source.objects.get(pk=source_id)
        review = Review.objects.get(pk=review_id)
        review.sources.remove(source)
        if not source.is_default:
            source.delete()
        review.save()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def add_suggested_sources(request):
    try:
        source_ids = request.POST.getlist('source-id')
        review_id = request.POST['review-id']
        review = Review.objects.get(pk=review_id)
        return_html = ''
        for source_id in source_ids:
            source = Source.objects.get(pk=source_id)
            review.sources.add(source)
            return_html += html_source(source)
        review.save()
        return HttpResponse(return_html)
    except:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def save_question(request):
    '''
        Function used via Ajax request only.
        This function takes a review question form and save on the database
    '''
    try:
        prefix = str(request.POST['prefix'])
        review_id = request.POST['review-id']
        question_id = request.POST['question-id']
        question_type = request.POST['question-type']

        description = request.POST[prefix + 'question-description']
        population = request.POST[prefix + 'question-population']
        intervention = request.POST[prefix + 'question-intervention']
        comparison = request.POST[prefix + 'question-comparison']
        outcome = request.POST[prefix + 'question-outcome']

        review = Review.objects.get(pk=review_id)

        question = Question()

        if question_type == 'M':
            question = review.get_main_question()
        elif question_id != 'None':
            try:
                question = Question.objects.get(pk=question_id)
            except Question.DoesNotExist:
                pass

        question.review = review
        question.question = description
        question.population = population
        question.intervention = intervention
        question.comparison = comparison
        question.outcome = outcome
        question.question_type = question_type
        question.save()
        return HttpResponse(question.id)
    except:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def add_question(request):
    '''
        Function used via Ajax request only.
        This functions adds a new secondary question to the review.
    '''
    try:
        review_id = request.GET['review-id']
        review = Review.objects.get(pk=review_id)
        question = Question()
        prefix = int(time.time())
        context = RequestContext(request, {'review': review, 'question': question, 'question_type':'S', 'prefix':prefix})
        return render_to_response('reviews/planning_question.html', context)
    except:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def remove_question(request):
    '''
        Function used via Ajax request only.
        This function removes a secondary question from the review.
    '''
    try:
        review_id = request.POST['review-id']
        question_id = request.POST['question-id']
        question_type = request.POST['question-type']
        if question_id != 'None' and question_type != 'M':
            try:
                question = Question.objects.get(pk=question_id)
                question.delete()
            except Question.DoesNotExist:
                return HttpResponseBadRequest()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def save_objective(request):
    try:
        review_id = request.POST['review-id']
        objective = request.POST['objective']
        review = Review.objects.get(pk=review_id)
        review.objective = objective
        review.save()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def add_criteria(request):
    try:
        review_id = request.GET['review-id']
        description = request.GET['criteria']
        criteria_type = request.GET['criteria-type']
        review = Review.objects.get(pk=review_id)
        criteria = SelectionCriteria(review=review, description=description, criteria_type=criteria_type)
        criteria.save()
        return HttpResponse('<option value="' + str(criteria.id) + '">' + escape(criteria.description) + '</option>')
    except:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def remove_criteria(request):
    try:
        review_id = request.GET['review-id']
        review = Review.objects.get(pk=review_id)
        criteria_ids = request.GET['criteria-ids']
        ids = criteria_ids.split(',')
        for id in ids:
            criteria = SelectionCriteria.objects.get(pk=id)
            criteria.delete()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def add_synonym(request):
    try:
        review_id = request.GET['review-id']
        keyword_id = request.GET['keyword-id']
        description = request.GET['synonym']
        review = Review.objects.get(pk=review_id)
        keyword = Keyword.objects.get(pk=keyword_id)
        synonym = Keyword(review=review, synonym_of=keyword, description=description)
        synonym.save()
        return HttpResponse('<li synonym-id="' + str(synonym.id) + '">' + escape(synonym.description) + '</li>')
    except:
        return HttpResponseBadRequest()

def extract_keywords(keywords, review):
    keyword_list = keywords.split(',')
    keyword_objects = []
    for term in keyword_list:
        if len(term) > 0:
            keyword = Keyword(review=review, description=term.strip())
            keyword.save()
            keyword_objects.append(keyword)
    return keyword_objects

@ajax_required
@author_required
@login_required
def import_pico_keywords(request):
    try:
        review_id = request.GET['review-id']
        review = Review.objects.get(pk=review_id)
        questions = review.get_questions()
        keywords = []

        for question in questions:
            keywords += extract_keywords(question.population, review)
            keywords += extract_keywords(question.intervention, review)
            keywords += extract_keywords(question.comparison, review)
            keywords += extract_keywords(question.outcome, review)

        str_return = ""

        for keyword in keywords:
            str_return += '''
            <tr keyword-id="''' + str(keyword.id) + '''">
              <td class="keyword-row">''' + escape(keyword.description) + '''</td>
              <td>
                <ul></ul>
                <input type="text" class="add-synonym">
              </td>
              <td><button type="button" class="btn btn-small btn-warning btn-remove-keyword">remove</button></td>
              <td class="no-border"></td>
            </tr>'''
        return HttpResponse(str_return)
    except:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def remove_keyword(request):
    try:
        review_id = request.GET['review-id']
        keyword_id = request.GET['keyword-id']
        review = Review.objects.get(pk=review_id)
        keyword = Keyword.objects.get(pk=keyword_id)
        synonyms = Keyword.objects.filter(synonym_of__id=keyword_id)
        for synonym in synonyms:
            synonym.delete()
        keyword.delete()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def add_new_keyword(request):
    try:
        review_id = request.GET['review-id']
        description = request.GET['description']
        review = Review.objects.get(pk=review_id)
        keyword = Keyword(review=review, description=description)
        keyword.save()
        str_return = '''
        <tr keyword-id="''' + str(keyword.id) + '''">
          <td class="keyword-row">''' + escape(keyword.description) + '''</td>
          <td>
            <ul></ul>
            <input type="text" class="add-synonym">
          </td>
          <td><button type="button" class="btn btn-small btn-warning btn-remove-keyword">remove</button></td>
          <td class="no-border"></td>
        </tr>'''
        return HttpResponse(str_return)
    except:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def save_keyword(request):
    try:
        review_id = request.GET['review-id']
        keyword_id = request.GET['keyword-id']
        description = request.GET['description']
        review = Review.objects.get(pk=review_id)
        keyword = Keyword.objects.get(pk=keyword_id)
        keyword.description = description
        keyword.save()
        return HttpResponse(escape(keyword.description))
    except:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def save_synonym(request):
    try:
        review_id = request.GET['review-id']
        synonym_id = request.GET['synonym-id']
        description = request.GET['description']
        review = Review.objects.get(pk=review_id)
        synonym = Keyword.objects.get(pk=synonym_id)
        if (len(description) == 0):
            synonym.delete()
            return HttpResponse()
        else:
            synonym.description = description
            synonym.save()
            return HttpResponse(escape(synonym.description))
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
        if review.is_author_or_coauthor(request.user):
            review.description = description
            review.save()
            return HttpResponse()
        else:
           return HttpResponseForbidden()
    except:
        return HttpResponseBadRequest()

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
    if review.is_author_or_coauthor(request.user):
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

            for keyword in population_list:
                query_population.append(keyword)
                synonyms = filter(lambda s: s.synonym_of is not None and s.synonym_of.description == keyword, keywords)
                for synonym in synonyms:
                    query_population.append(synonym.description)

            for keyword in intervention_list:
                query_intervention.append(keyword)
                synonyms = filter(lambda s: s.synonym_of is not None and s.synonym_of.description == keyword, keywords)
                for synonym in synonyms:
                    query_intervention.append(synonym.description)

            for keyword in comparison_list:
                query_comparison.append(keyword)
                synonyms = filter(lambda s: s.synonym_of is not None and s.synonym_of.description == keyword, keywords)
                for synonym in synonyms:
                    query_comparison.append(synonym.description)

            for keyword in outcome_list:
                query_outcome.append(keyword)
                synonyms = filter(lambda s: s.synonym_of is not None and s.synonym_of.description == keyword, keywords)
                for synonym in synonyms:
                    query_outcome.append(synonym.description)


        str_population = ' OR '.join(query_population)
        str_intervention = ' OR '.join(query_intervention)
        str_comparison = ' OR '.join(query_comparison)
        str_outcome = ' OR '.join(query_outcome)

        search_string = []
        if str_population:
            search_string.append('(' + str_population + ')')
        if str_intervention:
            search_string.append('(' + str_intervention + ')')
        if str_comparison:
            search_string.append('(' + str_comparison + ')')
        if str_outcome:
            search_string.append('(' + str_outcome + ')')

        return HttpResponse(' AND '.join(search_string))
    return HttpResponse('')