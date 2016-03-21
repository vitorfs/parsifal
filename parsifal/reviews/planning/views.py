# coding: utf-8

import time
import json

from django.db import transaction
from django.core.urlresolvers import reverse as r
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.utils.html import escape

from parsifal.reviews.models import *
from parsifal.reviews.planning.forms import KeywordForm, SynonymForm
from parsifal.reviews.decorators import main_author_required, author_required


@author_required
@login_required
def planning(request, username, review_name):
    return redirect(r('protocol', args=(username, review_name)))

@author_required
@login_required
def protocol(request, username, review_name):
    review = get_object_or_404(Review, name=review_name, author__username__iexact=username)
    return render(request, 'planning/protocol.html', { 'review': review })

@author_required
@login_required
def quality_assessment_checklist(request, username, review_name):
    review = get_object_or_404(Review, name=review_name, author__username__iexact=username)
    return render(request, 'planning/quality_assessment_checklist.html', { 'review': review })

@author_required
@login_required
def data_extraction_form(request, username, review_name):
    review = get_object_or_404(Review, name=review_name, author__username__iexact=username)
    empty_field = DataExtractionField()
    return render(request, 'planning/data_extraction_form.html', { 'review': review, 'empty_field': empty_field })


'''
    OBJECTIVE FUNCTIONS
'''

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


'''
    QUESTION FUNCTIONS
'''

@author_required
@login_required
def save_question(request):
    '''
        Function used via Ajax request only.
        This function takes a review question form and save on the database
    '''
    try:
        review_id = request.POST['review-id']
        question_id = request.POST['question-id']
        description = request.POST['description']
        review = Review.objects.get(pk=review_id)
        try:
            question = Question.objects.get(pk=question_id)
        except:
            question = Question(review=review)
        question.question = description[:500]
        question.save()
        context = RequestContext(request, {'question':question})
        return render_to_response('planning/partial_planning_question.html', context)
    except:
        return HttpResponseBadRequest()

@author_required
@login_required
def save_question_order(request):
    try:
        orders = request.POST.get('orders')
        question_orders = orders.split(',')
        for question_order in question_orders:
            if question_order:
                question_id, order = question_order.split(':')
                question = Question.objects.get(pk=question_id)
                question.order = order
                question.save()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()

@author_required
@login_required
def add_or_edit_question(request):
    '''
        Function used via Ajax request only.
        This functions adds a new secondary question to the review.
    '''
    try:
        review_id = request.POST['review-id']
        question_id = request.POST['question-id']
        review = Review.objects.get(pk=review_id)
        try:
            question = Question.objects.get(pk=question_id)
        except:
            question = Question(review=review)
        context = RequestContext(request, {'question':question})
        return render_to_response('planning/partial_planning_question_form.html', context)
    except:
        return HttpResponseBadRequest()


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
        if question_id != 'None':
            try:
                question = Question.objects.get(pk=question_id)
                question.delete()
            except Question.DoesNotExist:
                return HttpResponseBadRequest()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()


'''
    PICOC FUNCTIONS
'''

@author_required
@login_required
def save_picoc(request):
    try:
        review_id = request.POST['review-id']
        review = Review.objects.get(pk=review_id)
        review.population = request.POST['population'][:200]
        review.intervention = request.POST['intervention'][:200]
        review.comparison = request.POST['comparison'][:200]
        review.outcome = request.POST['outcome'][:200]
        review.context = request.POST['context'][:200]
        review.save()
        return HttpResponse()
    except Exception, e:
        return HttpResponseBadRequest()


'''
    KEYWORDS/SYNONYM FUNCTIONS
'''

def extract_keywords(review, pico):
    if pico == Keyword.POPULATION: keywords = review.population
    elif pico == Keyword.INTERVENTION: keywords = review.intervention
    elif pico == Keyword.COMPARISON: keywords = review.comparison
    elif pico == Keyword.OUTCOME: keywords = review.outcome
    keyword_list = keywords.split(',')
    keyword_objects = []
    for term in keyword_list:
        if len(term) > 0:
            keyword = Keyword(review=review, description=term.strip(), related_to=pico)
            if keyword.description not in review.get_keywords().values_list('description', flat=True):
                keyword.save()
                keyword_objects.append(keyword)
    return keyword_objects


@author_required
@login_required
def import_pico_keywords(request):
    try:
        review_id = request.GET['review-id']
        review = Review.objects.get(pk=review_id)
        keywords = []

        keywords += extract_keywords(review, Keyword.POPULATION)
        keywords += extract_keywords(review, Keyword.INTERVENTION)
        keywords += extract_keywords(review, Keyword.COMPARISON)
        keywords += extract_keywords(review, Keyword.OUTCOME)

        html = u''

        for keyword in keywords:
            context = RequestContext(request, { 'keyword': keyword })
            html += render_to_string('planning/partial_keyword.html', context)
        return HttpResponse(html)
    except:
        return HttpResponseBadRequest()


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

@transaction.atomic
@author_required
@login_required
def add_keyword(request):
    review_id = request.GET.get('review-id', request.POST.get('review-id'))
    review = Review.objects.get(pk=review_id)
    SynonymFormSet = formset_factory(SynonymForm)
    response = {}
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        formset = SynonymFormSet(request.POST, prefix='synonym')
        if form.is_valid() and formset.is_valid():
            form.instance.review = review
            keyword = form.save()
            for form in formset:
                if form.instance.description:
                    form.instance.review = review
                    form.instance.synonym_of = keyword
                    form.save()
            context = RequestContext(request, { 'keyword': keyword })
            response['status'] = 'ok'
            response['html'] = render_to_string('planning/partial_keyword.html', context)
            dump = json.dumps(response)
            return HttpResponse(dump, content_type='application/json')
        else:
            response['status'] = 'validation_error'
    else:
        form = KeywordForm()
        formset = SynonymFormSet(prefix='synonym')
        response['status'] = 'new'
    context = RequestContext(request, {
            'review': review,
            'form': form,
            'formset': formset
        })
    response['html'] = render_to_string('planning/partial_keyword_form.html', context)
    dump = json.dumps(response)
    return HttpResponse(dump, content_type='application/json')

@transaction.atomic
@author_required
@login_required
def edit_keyword(request):
    review_id = request.GET.get('review-id', request.POST.get('review-id'))
    keyword_id = request.GET.get('keyword-id', request.POST.get('keyword-id'))
    review = Review.objects.get(pk=review_id)
    keyword = Keyword.objects.get(pk=keyword_id)

    SynonymFormSet = inlineformset_factory(Keyword, Keyword, SynonymForm, extra=1)
    response = {}
    if request.method == 'POST':
        form = KeywordForm(request.POST, instance=keyword)
        formset = SynonymFormSet(request.POST, instance=keyword, prefix='synonym')
        if form.is_valid() and formset.is_valid():
            form.instance.review = review
            keyword = form.save()
            for form in formset:
                form.instance.review = review
                form.instance.synonym_of = keyword
            formset.save()
            context = RequestContext(request, { 'keyword': keyword })
            response['status'] = 'ok'
            response['html'] = render_to_string('planning/partial_keyword.html', context)
            dump = json.dumps(response)
            return HttpResponse(dump, content_type='application/json')
        else:
            response['status'] = 'validation_error'
    else:
        form = KeywordForm(instance=keyword)
        formset = SynonymFormSet(instance=keyword, prefix='synonym')
        response['status'] = 'new'
    context = RequestContext(request, {
            'review': review,
            'form': form,
            'formset': formset
        })
    response['html'] = render_to_string('planning/partial_keyword_form.html', context)
    dump = json.dumps(response)
    return HttpResponse(dump, content_type='application/json')

'''
    SEARCH STRING FUNCTIONS
'''

@author_required
@login_required
def generate_search_string(request):
    '''
        Function used via Ajax request only.
        Still have to refactor this function. This is just a first approach.
    '''
    review_id = request.GET['review-id']
    review = Review.objects.get(pk=review_id)

    keywords = []
    for key, value in Keyword.RELATED_TO:
        synonyms = []
        for keyword in review.keywords.filter(related_to=key, synonym_of=None):
            synonyms.append(u'"{0}"'.format(keyword.description))
            for synonym in keyword.synonyms.all():
                synonyms.append(u'"{0}"'.format(synonym.description))
        if any(synonyms):
            keywords.append(u'({0})'.format(u' OR '.join(synonyms)))

    return HttpResponse(' AND '.join(keywords))


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


'''
    SOURCE FUNCTIONS
'''

def html_source(source):
    html = '<tr source-id="' + str(source.id) + '"><td>' + escape(source.name) + '</td>'
    if source.url:
        html += '<td><a href="' + escape(source.url) + '" target="_blank">' + escape(source.url) + '</a></td>'
    else:
        html += '<td>' + escape(source.url) + '</td>'
    if source.is_default:
        html += '<td class="text-right"><span data-toggle="tooltip" data-placement="top" data-container="body" title="It\'s not possible to edit Digital Library\'s details"><button type="button" class="btn btn-sm btn-warning" disabled>edit</button></span> <button type="button" class="btn btn-danger btn-sm js-start-remove">remove</a></td></tr>'
    else:
        html += '<td class="text-right"><button type="button" class="btn btn-sm btn-warning btn-edit-source"><span class="glyphicon glyphicon-pencil"></span> edit</button> <button type="button" class="btn btn-danger btn-sm js-start-remove"><span class="glyphicon glyphicon-trash"></span> remove</a></td></tr>'
    return html


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
        name = request.GET['name'][:100]
        url = request.GET['url'][:200]

        review = Review.objects.get(pk=review_id)
        if source_id:
            try:
                source = Source.objects.get(pk=source_id)
                source.name = name
                source.set_url(url)
                source.save()
                review.sources.add(source)
                review.save()
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
    except Exception, e:
        return HttpResponseBadRequest()


@author_required
@login_required
def remove_source_from_review(request):
    try:
        source_id = request.GET['source-id']
        review_id = request.GET['review-id']
        source = Source.objects.get(pk=source_id)
        review = Review.objects.get(pk=review_id)
        review.sources.remove(source)
        if source.is_default:
            review.get_source_articles(source.id).delete()
            try:
                review.searchsession_set.filter(source=source).delete()
            except:
                pass
        else:
            source.delete()
        review.save()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()


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


'''
    INCLUSION/EXCLUSION CRITERIA FUNCTIONS
'''

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


'''
    QUALITY ASSESSMENT FUNCTIONS
'''

@author_required
@login_required
def add_quality_assessment_question(request):
    try:
        quality_question = QualityQuestion()
        context = RequestContext(request, {'quality_question': quality_question})
        return render_to_response('planning/partial_quality_assessment_question_form.html', context)
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def edit_quality_assessment_question(request):
    try:
        quality_question_id = request.GET['quality-question-id']
        quality_question = QualityQuestion.objects.get(pk=quality_question_id)
        context = RequestContext(request, {'quality_question': quality_question})
        return render_to_response('planning/partial_quality_assessment_question_form.html', context)
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def save_quality_assessment_question(request):
    try:
        description = request.POST['description']
        review_id = request.POST['review-id']
        quality_question_id = request.POST['quality-question-id']

        review = Review.objects.get(pk=review_id)

        if quality_question_id == 'None':
            quality_question = QualityQuestion(review=review)
        else:
            quality_question = QualityQuestion.objects.get(pk=quality_question_id)

        quality_question.description = description
        quality_question.save()

        context = RequestContext(request, {'quality_question': quality_question})
        return render_to_response('planning/partial_quality_assessment_question.html', context)
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def save_quality_assessment_question_order(request):
    try:
        orders = request.POST.get('orders')
        question_orders = orders.split(',')
        for question_order in question_orders:
            if question_order:
                question_id, order = question_order.split(':')
                question = QualityQuestion.objects.get(pk=question_id)
                question.order = order
                question.save()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def remove_quality_assessment_question(request):
    try:
        quality_question_id = request.GET['quality-question-id']
        quality_question = QualityQuestion.objects.get(pk=quality_question_id)
        quality_question.delete()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def add_quality_assessment_answer(request):
    try:
        quality_answer = QualityAnswer()
        context = RequestContext(request, {'quality_answer': quality_answer})
        return render_to_response('planning/partial_quality_assessment_answer_form.html', context)
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def edit_quality_assessment_answer(request):
    try:
        quality_answer_id = request.GET['quality-answer-id']
        quality_answer = QualityAnswer.objects.get(pk=quality_answer_id)
        context = RequestContext(request, {'quality_answer': quality_answer})
        return render_to_response('planning/partial_quality_assessment_answer_form.html', context)
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def save_quality_assessment_answer(request):
    try:
        description = request.POST['description']
        weight = request.POST['weight']
        review_id = request.POST['review-id']
        quality_answer_id = request.POST['quality-answer-id']

        weight = weight.replace(',', '.')
        try:
            weight = float(weight)
        except:
            weight = 0.0

        review = Review.objects.get(pk=review_id)

        if quality_answer_id == 'None':
            quality_answer = QualityAnswer(review=review)
        else:
            quality_answer = QualityAnswer.objects.get(pk=quality_answer_id)

        quality_answer.description = description
        quality_answer.weight = weight
        quality_answer.save()

        context = RequestContext(request, {'quality_answer': quality_answer})
        return render_to_response('planning/partial_quality_assessment_answer.html', context)
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def remove_quality_assessment_answer(request):
    try:
        quality_answer_id = request.GET['quality-answer-id']
        quality_answer = QualityAnswer.objects.get(pk=quality_answer_id)
        quality_answer.delete()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def add_suggested_answer(request):
    try:
        review_id = request.GET['review-id']
        review = Review.objects.get(pk=review_id)
        if not review.get_quality_assessment_answers():
            html_answers = u''
            for answer, value in QualityAnswer.SUGGESTED_ANSWERS:
                quality_answer = QualityAnswer(review=review, description=answer, weight=value)
                quality_answer.save()
                html_answers += '''<tr oid="{0}">
                  <td>{1}</td>
                  <td>{2}</td>
                  <td>
                    <button type="button" class="btn btn-warning btn-sm btn-edit-quality-answer">edit</button>
                    <button type="button" class="btn btn-danger btn-sm btn-remove-quality-answer">remove</button>
                  </td>
                </tr>'''.format(quality_answer.id, quality_answer.description, quality_answer.weight)
            return HttpResponse(html_answers)
        else:
            return HttpResponseBadRequest()
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def calculate_max_score(request):
    try:
        review_id = request.GET['review-id']
        review = Review.objects.get(pk=review_id)
        max_score = review.calculate_quality_assessment_max_score()
        return HttpResponse(max_score)
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def save_cutoff_score(request):
    try:
        review_id = request.GET['review-id']
        cutoff_score = request.GET['cutoff-score']
        review = Review.objects.get(pk=review_id)
        review.quality_assessment_cutoff_score = float(cutoff_score)
        review.save()
        return HttpResponse('Cutoff score saved successfully!')
    except:
        return HttpResponseBadRequest('Invalid value.')


'''
    DATA EXTRACTION FUNCTIONS
'''

@author_required
@login_required
def add_new_data_extraction_field(request):
    field = DataExtractionField()
    context = RequestContext(request, {'field': field})
    return render_to_response('planning/partial_data_extraction_field_form.html', context)


@author_required
@login_required
def edit_data_extraction_field(request):
    field_id = request.GET['field-id']
    field = DataExtractionField.objects.get(pk=field_id)
    context = RequestContext(request, {'field': field})
    return render_to_response('planning/partial_data_extraction_field_form.html', context)


@author_required
@login_required
def save_data_extraction_field(request):
    try:
        review_id = request.POST['review-id']
        description = request.POST['description']
        field_type = request.POST['field-type']
        lookup_values = request.POST['lookup-values']
        field_id = request.POST['field-id']

        if not field_type and not description:
            return HttpResponseBadRequest('Description and Type are required fields.')

        lookup_values = lookup_values.split('\n')
        lookup_values = list(set(lookup_values))

        for i in range(0, len(lookup_values)):
            lookup_values[i] = lookup_values[i].strip()

        review = Review.objects.get(pk=review_id)

        if field_id == 'None':
            field = DataExtractionField(review=review)
        else:
            field = DataExtractionField.objects.get(pk=field_id)
            if field.field_type != field_type:
                try:
                    data_extractions = DataExtraction.objects.filter(field__id=field_id)
                    for data_extraction in data_extractions:
                        data_extraction.value = ''
                        data_extraction.select_values.clear()
                        data_extraction.save()
                except Exception, e:
                    pass

        field.description = description
        field.field_type = field_type
        field.save()

        if field.is_select_field():
            for value in lookup_values:
                if value:
                    lookup_value, created = DataExtractionLookup.objects.get_or_create(field=field, value=value)

            for select_value in field.get_select_values():
                if select_value.value not in lookup_values:
                    select_value.delete()
        else:
            for select_value in field.get_select_values():
                select_value.delete()

        context = RequestContext(request, {'field': field})
        return render_to_response('planning/partial_data_extraction_field.html', context)
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def save_data_extraction_field_order(request):
    try:
        orders = request.POST.get('orders')
        field_orders = orders.split(',')
        for field_order in field_orders:
            if field_order:
                field_id, order = field_order.split(':')
                field = DataExtractionField.objects.get(pk=field_id)
                field.order = order
                field.save()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def remove_data_extraction_field(request):
    try:
        field_id = request.GET['field-id']
        field = DataExtractionField.objects.get(pk=field_id)
        select_values = field.get_select_values()
        for select_value in select_values:
            select_value.delete()
        field.delete()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()
