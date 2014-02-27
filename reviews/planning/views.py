# coding: utf-8
import time
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.utils.html import escape
from reviews.models import Review, Source, Question, SelectionCriteria, Keyword, DataExtractionFields, DataExtractionLookups
from reviews.decorators import main_author_required, author_required
from parsifal.decorators import ajax_required

@login_required
def planning(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username=username)
    context = RequestContext(request, {'review': review })
    return render_to_response('planning/planning.html', context)


###############################################################################
# OBJECTIVE FUNCTIONS 
###############################################################################

@ajax_required
@author_required
@login_required
def save_objective(request):
    try:
        review_id = request.POST['review-id']
        objective = request.POST['objective']
        review = Review.objects.get(pk=review_id)
        if len(objective) > 1000:
            return HttpResponseBadRequest('The review objectives should not exceed 1000 characters. The given objectives have %s characters.' % len(objective))
        else:
            review.objective = objective
            review.save()
            return HttpResponse('Your review have been saved successfully!')
    except:
        return HttpResponseBadRequest()


###############################################################################
# QUESTION FUNCTIONS 
###############################################################################

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

        if question_type == Question.MAIN:
            question = review.get_main_question()
        elif question_id != 'None':
            try:
                question = Question.objects.get(pk=question_id)
            except Question.DoesNotExist:
                pass

        question.review = review

        if len(description) <= 500:
            question.question = description
        else:
            return HttpResponseBadRequest('The question description should not exceed 500 characters. The given description have %s characters.' % len(description))

        question.population = population
        question.intervention = intervention
        question.comparison = comparison
        question.outcome = outcome

        if filter(lambda q: q[0] == question_type, Question.QUESTION_TYPES):
            question.question_type = question_type
        else:
           return HttpResponseBadRequest('Invalid question type.') 

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
        context = RequestContext(request, {'review': review, 'question': question, 'question_type':Question.SECONDARY, 'prefix':prefix})
        return render_to_response('planning/partial_planning_question.html', context)
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
        if question_id != 'None' and question_type != Question.MAIN:
            try:
                question = Question.objects.get(pk=question_id)
                question.delete()
            except Question.DoesNotExist:
                return HttpResponseBadRequest()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()


###############################################################################
# KEYWORDS/SYNONYM FUNCTIONS 
###############################################################################

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
                <input type="text" class="add-synonym" maxlength="200">
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
            <input type="text" class="add-synonym" maxlength="200">
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


###############################################################################
# SOURCE FUNCTIONS 
###############################################################################

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
def suggested_sources(request):
    try:
        review_id = request.GET['review-id']
        review = Review.objects.get(pk=review_id)
        review.sources
        default_sources = Source.objects.filter(is_default=True)
        sources = filter(lambda s: s not in review.sources.all(), default_sources)
        return_html = ''
        for source in sources:
            return_html += '''
            <tr>
              <td>
                <input type="checkbox" value="''' + str(source.id) + '''" name="source-id">
              </td>
              <td>''' + str(source.name) + '''</td>
              <td>
                <a href="''' + source.url + '''" target="_blank">''' + source.url + '''</a>
              </td>
            </tr>'''
        return HttpResponse(return_html)
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


###############################################################################
# INCLUSION/EXCLUSION CRITERIA FUNCTIONS 
###############################################################################

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


###############################################################################
# DATA EXTRACTION FUNCTIONS 
###############################################################################

@ajax_required
@author_required
@login_required
def add_new_data_extraction_field(request):
    field = DataExtractionFields()
    context = RequestContext(request, {'field': field, 'data_extraction_field_types': DataExtractionFields.FIELD_TYPES})
    return render_to_response('planning/partial_data_extraction_field_form.html', context)

@ajax_required
@author_required
@login_required
def save_data_extraction_field(request):
    try:
        review_id = request.POST['review-id']
        description = request.POST['description']
        field_type = request.POST['field-type']
        lookup_values = request.POST['lookup-values']

        lookup_values = lookup_values.split('\n')

        review = Review.objects.get(pk=review_id)
        field = DataExtractionFields(description=description, field_type=field_type, review=review)
        field.save()

        for value in lookup_values:
            if value.strip():
                lookup_value = DataExtractionLookups(field=field, value=value.strip())
                lookup_value.save()

        context = RequestContext(request, {'field': field})
        return render_to_response('planning/partial_data_extraction_field.html', context)
    except:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def remove_data_extraction_field(request):
    try:
        field_id = request.GET['field-id']
        field = DataExtractionFields.objects.get(pk=field_id)
        select_values = field.get_select_values()
        for select_value in select_values:
            select_value.delete()
        field.delete()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def edit_data_extraction_field(request):
    field_id = request.GET['field-id']
    field = DataExtractionFields.objects.get(pk=field_id)
    context = RequestContext(request, {'field': field, 'data_extraction_field_types': DataExtractionFields.FIELD_TYPES})
    return render_to_response('planning/partial_data_extraction_field_form.html', context)