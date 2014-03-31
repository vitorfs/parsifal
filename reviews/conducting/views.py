# coding: utf-8
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect, get_object_or_404, render
from django.template import RequestContext
from reviews.models import *
from reviews.decorators import main_author_required, author_required
from parsifal.decorators import ajax_required
from bibtexparser.bparser import BibTexParser
from django.conf import settings as django_settings
from django.core.context_processors import csrf

@author_required
@login_required
def conducting(request, username, review_name):
    return redirect('/' + username + '/' + review_name + '/conducting/search/')

@author_required
@login_required
def search_string(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username__iexact=username)
    context = RequestContext(request, {'review': review})
    return render_to_response('conducting/conducting_search_string.html', context)

@author_required
@login_required
def study_selection(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username__iexact=username)
    try:
        active_tab = int(request.GET['source'])
    except Exception, e:
        active_tab = -1

    context = RequestContext(request, {'review': review, 'active_tab': active_tab})
    return render_to_response('conducting/conducting_study_selection.html', context)

def get_workflow_steps(self, review):
    pass

def build_quality_assessment_table(request, review):
    selected_studies = review.get_accepted_articles()
    quality_questions = review.get_quality_assessment_questions()
    quality_answers = review.get_quality_assessment_answers()

    if quality_questions and quality_answers:
        str_table = ''
        for study in selected_studies:
            str_table += '''<table class="table" id="tbl-quality" article-id="''' + str(study.id) + '''" csrf-token="''' + unicode(csrf(request)['csrf_token']) +'''">
                <thead>
                <tr>
                  <th colspan="'''+ str(quality_answers.count() + 1) + '''">''' + study.title + '''</th>
                </tr>
                </thead>
                <tfoot>
                <tr>
                  <th></th>
                  <th colspan="'''+ str(quality_answers.count()) + '''">Quality Score: <span class="score">'''+ str(study.get_score()) + '''</span></th>
                </tr>
                </tfoot>
                <tbody>'''
            quality_assessment = study.get_quality_assesment()
            for question in quality_questions:
                str_table += '''<tr question-id="''' + str(question.id) + '''">
                <td>''' + question.description + '''</td>'''
                
                try:
                    question_answer = quality_assessment.filter(question__id=question.id).get()
                except:
                    question_answer = None

                for answer in quality_answers:
                    selected_answer = ''
                    if question_answer is not None:
                        if answer.id == question_answer.answer.id:
                            selected_answer = ' selected-answer'
                    str_table += '''<td class="answer'''+ selected_answer +'''" answer-id="''' + str(answer.id) + '''">''' + answer.description + '''</td>'''
                str_table += '''</tr>'''
            str_table += '''</tbody></table>'''
        return str_table
    else:
        return ''

@author_required
@login_required
def quality_assessment(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username__iexact=username)

    add_sources = review.sources.count()
    import_articles = review.get_source_articles().count()
    select_articles = review.get_accepted_articles().count()
    create_questions = review.get_quality_assessment_questions().count()
    create_answers = review.get_quality_assessment_answers().count()

    steps_messages = []

    if not add_sources: steps_messages.append('Use the <a href="/'+ username +'/'+ review_name +'/planning/">planning tab</a> to add sources to your review.')
    if not import_articles: steps_messages.append('Import the studies using the <a href="/'+ username +'/'+ review_name +'/conducting/studies/">study selection tab</a>.')
    if not select_articles: steps_messages.append('Classify the imported studies using the <a href="/'+ username +'/'+ review_name +'/conducting/studies/">study selection tab</a>.')
    if not create_questions: steps_messages.append('Create quality assessment questions using the <a href="/'+ username +'/'+ review_name +'/planning/">planning tab</a>.')
    if not create_answers: steps_messages.append('Create quality assessment answers using the <a href="/'+ username +'/'+ review_name +'/planning/">planning tab</a>.')

    finished_all_steps = len(steps_messages) == 0

    quality_assessment_table = build_quality_assessment_table(request, review)

    context = RequestContext(request, {'review': review, 'steps_messages': steps_messages, 'quality_assessment_table': quality_assessment_table, 'finished_all_steps': finished_all_steps})
    return render_to_response('conducting/conducting_quality_assessment.html', context)

def build_data_extraction_field_row(article, field):
    str_field = u''

    try:
        extraction = DataExtraction.objects.get(article=article, field=field)
    except Exception, e:
        extraction = None

    if field.field_type == field.BOOLEAN_FIELD:
        true = u''
        false = u''
        if extraction != None:
            if extraction.get_value() == True:
                true = u' selected'
            elif extraction.get_value() == False:
                false = u' selected'

        str_field = u'''<select name="value">
            <option value="">Select...</option>
            <option value="True"{0}>True</option>
            <option value="False"{1}>False</option>
          </select>'''.format(true, false)

    elif field.field_type == field.DATE_FIELD:
        if extraction != None:
            value = extraction.get_date_value_as_string()
        else:
            value = u''
        str_field = u'<input type="text" name="{0}-{1}-value" maxlength="10" value="{2}">'.format(article.id, field.id, value)

    elif field.field_type == field.SELECT_ONE_FIELD:
        str_field = u'''<select name="{0}-{1}-value">
            <option value="">Select...</option>'''.format(article.id, field.id)
        for value in field.get_select_values():
            if extraction != None and extraction.get_value() != None and extraction.get_value().id == value.id:
                selected = ' selected'
            else:
                selected = ''
            str_field += u'''<option value="{0}"{1}>{2}</option>'''.format(value.id, selected, value.value)
        str_field += u'</select>'

    elif field.field_type == field.SELECT_MANY_FIELD:
        for value in field.get_select_values():
            if extraction != None and value in extraction.get_value():
                checked = ' checked'
            else:
                checked = ''
            str_field += u'<input type="checkbox" name="{0}-{1}-value" value="{2}"{3}>{4} '.format(article.id, field.id, value.id, checked, value.value)

    else:
        if extraction != None:
            value = extraction.get_value()
        else:
            value = u''
        str_field = u'<input type="text" name="{0}-{1}-value" maxlength="1000" value="{2}">'.format(article.id, field.id, value)

    return str_field

def build_data_extraction_table(review):
    selected_studies = review.get_final_selection_articles()
    data_extraction_fields = review.get_data_extraction_fields()
    if data_extraction_fields:
        str_table = u''
        for study in selected_studies:
            str_table += u'''<div class="container data-extraction-container"><table class="table tbl-data-extraction" article-id="{0}">
                <thead>
                  <tr>
                    <th colspan="2">{1} <span class="label label-success pull-right">{2}</span></th>
                  </tr>
                </thead>
                <tbody>'''.format(study.id, study.title, study.get_score())
            for field in data_extraction_fields:
                str_table += u'''<tr field-id="{0}">
                  <td style="width: 25%;" class="data-extraction-label">{1}</td>
                  <td style="width: 75%;">{2}<p class="error hide"></p></td>
                </tr>'''.format(field.id, field.description, build_data_extraction_field_row(study, field))
            str_table += u'</tbody></table></div>'
        return str_table
    else:
        return u''

@author_required
@login_required
def data_extraction(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username__iexact=username)

    add_sources = review.sources.count()
    import_articles = review.get_source_articles().count()
    select_articles = review.get_accepted_articles().count()
    create_questions = review.get_quality_assessment_questions().count()
    create_answers = review.get_quality_assessment_answers().count()
    create_fields = review.get_data_extraction_fields().count()

    steps_messages = []

    if not add_sources: steps_messages.append('Use the <a href="/'+ username +'/'+ review_name +'/planning/">planning tab</a> to add sources to your review.')
    if not import_articles: steps_messages.append('Import the studies using the <a href="/'+ username +'/'+ review_name +'/conducting/studies/">study selection tab</a>.')
    if not select_articles: steps_messages.append('Classify the imported studies using the <a href="/'+ username +'/'+ review_name +'/conducting/studies/">study selection tab</a>.')
    if not create_questions: steps_messages.append('Create quality assessment questions using the <a href="/'+ username +'/'+ review_name +'/planning/">planning tab</a>.')
    if not create_answers: steps_messages.append('Create quality assessment answers using the <a href="/'+ username +'/'+ review_name +'/planning/">planning tab</a>.')
    if not create_fields: steps_messages.append('Create data extraction fields using the <a href="/'+ username +'/'+ review_name +'/planning/">planning tab</a>.')

    finished_all_steps = len(steps_messages) == 0

    try:
        data_extraction_table = build_data_extraction_table(review)
    except Exception, e:
        data_extraction_table = '<h3>Something went wrong while rendering the data extraction form.</h3>'

    context = RequestContext(request, {'review': review, 'steps_messages': steps_messages, 'data_extraction_table': data_extraction_table, 'finished_all_steps': finished_all_steps })
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
    filehandler = open(filename, 'r')
    parser = BibTexParser(filehandler)
    record_list = parser.get_entry_list()

    articles = []
    for record in record_list:
        article = Article()
        try:
            if 'id' in record: article.bibtex_key = record['id'][:100]
            if 'title' in record: article.title = record['title'][:1000]
            if 'journal' in record: article.journal = record['journal'][:1000]
            if 'year' in record: article.year = record['year'][:10]
            if 'author' in record: article.author = record['author'][:1000]
            if 'abstract' in record: article.abstract = record['abstract'][:4000]
            if 'pages' in record: article.pages = record['pages'][:20]
            if 'volume' in record: article.volume = record['volume'][:100]
            if 'document_type' in record: article.document_type = record['document_type'][:100]
            article.review = Review(id=review_id)
            article.source = Source(id=source_id)
        except:
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
    filename = django_settings.FILE_UPLOAD_TEMP_DIR + request.user.username + '.bib'
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    articles = bibtex_to_article_object(filename, review_id, source_id)
    for article in articles:
        article.save()
    return redirect('/' + review.author.username + '/' + review.name + '/conducting/studies/?source=' + source_id)

@ajax_required
@author_required
@login_required
def source_articles(request):
    review_id = request.GET['review-id']
    source_id = request.GET['source-id']

    review = Review.objects.get(pk=review_id)
    if source_id != 'None':
        articles = review.get_source_articles(source_id)
        source = Source.objects.get(pk=source_id)
    else:
        articles = review.get_source_articles()
        source = Source()

    return render(request, 'conducting/partial_conducting_articles.html', {'review': review, 'source': source, 'articles': articles})

@ajax_required
@author_required
@login_required
def article_details(request):
    article_id = request.GET['article-id']
    article = Article.objects.get(pk=article_id)
    context = RequestContext(request, {'article': article})
    return render_to_response('conducting/partial_conducting_article_details.html', context)

def build_article_table_row(article):
    span_status = ''
    if article.status == Article.ACCEPTED:
        span_status += '<span class="label label-success">'
    elif article.status == Article.REJECTED or article.status == Article.DUPLICATED:
        span_status += '<span class="label label-warning">'
    else:
        span_status += '<span>'
    span_status += article.get_status_display() + '</span>'
    row = u'''<tr oid="{0}" article-status="{1}">
            <td><input type="checkbox" value="{0}""></td>
            <td>{2}</td>
            <td>{3}</td>
            <td>{4}</td>
            <td>{5}</td>
            <td>{6}</td>
            <td>{7}</td>
          </tr>'''.format(article.id,
            article.status,
            article.bibtex_key,
            article.title,
            article.author,
            article.journal,
            article.year,
            span_status)
    return row

@ajax_required
@author_required
@login_required
def save_article_details(request):
    if request.method == 'POST':
        try:
            article_id = request.POST['article-id']

            if article_id != 'None':
                article = Article.objects.get(pk=article_id)
            else:
                review_id = request.POST['review-id']
                source_id = request.POST['source-id']
                review = Review.objects.get(pk=review_id)
                source = Source.objects.get(pk=source_id)
                article = Article(review=review, source=source)

            article.bibtex_key = request.POST['bibtex-key'][:100]
            article.title = request.POST['title'][:1000]
            article.author = request.POST['author'][:1000]
            article.journal = request.POST['journal'][:1000]
            article.year = request.POST['year'][:10]
            article.pages = request.POST['pages'][:20]
            article.volume = request.POST['volume'][:100]
            article.author = request.POST['author'][:1000]
            article.abstract = request.POST['abstract'][:4000]
            article.document_type = request.POST['document-type'][:100]
            article.comments = request.POST['comments'][:4000]
            status = request.POST['status'][:1]
            if status in (Article.UNCLASSIFIED, Article.REJECTED, Article.ACCEPTED, Article.DUPLICATED):
                article.status = status

            article.save()

            return HttpResponse(build_article_table_row(article))
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

@author_required
@login_required
def save_quality_assessment(request):
    try:
        article_id = request.POST['article-id']
        question_id = request.POST['question-id']
        answer_id = request.POST['answer-id']

        article = Article.objects.get(pk=article_id)
        question = QualityQuestion.objects.get(pk=question_id)
        answer = QualityAnswer.objects.get(pk=answer_id)

        quality_assessment, created = QualityAssessment.objects.get_or_create(article=article, question=question)
        quality_assessment.answer = answer
        quality_assessment.save()

        return HttpResponse(article.get_score())
    except:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def quality_assessment_detailed(request):
    try:
        review_id = request.GET['review-id']
        review = Review.objects.get(pk=review_id)
        quality_assessment_table = build_quality_assessment_table(request, review)
        context = RequestContext(request, {'review': review, 'quality_assessment_table': quality_assessment_table})
        return render_to_response('conducting/partial_conducting_quality_assessment_detailed.html', context)
    except:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def quality_assessment_summary(request):
    try:
        review_id = request.GET['review-id']
        review = Review.objects.get(pk=review_id)
        context = RequestContext(request, {'review': review, })
        return render_to_response('conducting/partial_conducting_quality_assessment_summary.html', context)
    except:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def multiple_articles_action_remove(request):
    try:
        article_ids = request.POST['article_ids']
        article_ids_list = article_ids.split('|')
        if article_ids_list:
            Article.objects.filter(pk__in=article_ids_list).delete()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def multiple_articles_action_accept(request):
    try:
        article_ids = request.POST['article_ids']
        article_ids_list = article_ids.split('|')
        if article_ids_list:
            Article.objects.filter(pk__in=article_ids_list).update(status=Article.ACCEPTED)
        return HttpResponse()
    except:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def multiple_articles_action_reject(request):
    try:
        article_ids = request.POST['article_ids']
        article_ids_list = article_ids.split('|')
        if article_ids_list:
            Article.objects.filter(pk__in=article_ids_list).update(status=Article.REJECTED)
        return HttpResponse()
    except:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def articles_order_by(request):
    try:
        review_id = request.GET['review-id']
        source_id = request.GET['source-id']
        column = request.GET['column']

        asc = ''
        if column[0] == '-':
            asc = '-'
        column = column.replace('-', '')

        review = Review.objects.get(pk=review_id)
        if source_id != 'None':
            articles = review.get_source_articles(source_id).extra(select={'lower_column': 'lower('+ column +')'}).order_by(asc + 'lower_column')
            source = Source.objects.get(pk=source_id)
        else:
            articles = review.get_source_articles().extra(select={'lower_column': 'lower('+ column +')'}).order_by(asc + 'lower_column')
            source = Source()

        str_return = u'<tbody>'
        for article in articles:
            str_return += build_article_table_row(article)
        str_return += '</tbody>'
        return HttpResponse(str_return)
    except:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def save_data_extraction(request):
    try:
        article_id = request.POST['article-id']
        field_id = request.POST['field-id']
        value = request.POST['value']

        article = Article.objects.get(pk=article_id)
        field = DataExtractionField.objects.get(pk=field_id)
        if article.review.is_author_or_coauthor(request.user):
            data_extraction, created = DataExtraction.objects.get_or_create(article=article, field=field)
            data_extraction.set_value(value)
            data_extraction.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
    except Exception, e:
        return HttpResponseBadRequest(e)

@ajax_required
@author_required
@login_required
def find_duplicates(request):
    review_id = request.GET['review-id']
    review = Review.objects.get(pk=review_id)
    duplicates = review.get_duplicate_articles()
    context = RequestContext(request, {'duplicates': duplicates})
    return render_to_response('conducting/partial_conducting_find_duplicates.html', context)

@ajax_required
@author_required
@login_required
def resolve_duplicated(request):
    try:
        article_id = request.POST['article-id']
        article = Article.objects.get(pk=article_id)
        if article.review.is_author_or_coauthor(request.user):
            article.status = Article.DUPLICATED
            article.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
    except Exception, e:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def resolve_all(request):
    try:
        article_id_list = []
        review_id = request.POST['review-id']
        review = Review.objects.get(pk=review_id)
        duplicates = review.get_duplicate_articles()
        for duplicate in duplicates:
            for i in range(1, len(duplicate)):
                duplicate[i].status = Article.DUPLICATED
                duplicate[i].save()
                article_id_list.append(str(duplicate[i].id))
        return HttpResponse(','.join(article_id_list))
    except Exception, e:
        return HttpResponseBadRequest()

@ajax_required
@author_required
@login_required
def new_article(request):
    review_id = request.GET['review-id']
    source_id = request.GET['source-id']

    review = Review.objects.get(pk=review_id)
    source = Source.objects.get(pk=source_id)

    article = Article(review=review, source=source)

    context = RequestContext(request, {'article': article})
    return render_to_response('conducting/partial_conducting_article_details.html', context)