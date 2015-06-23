# coding: utf-8

import json
from bibtexparser.bparser import BibTexParser

from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse as r
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect, get_object_or_404, render
from django.template import RequestContext
from django.conf import settings as django_settings
from django.core.context_processors import csrf
from django.db.models import Count

from reviews.models import *
from reviews.decorators import main_author_required, author_required
from reviews.forms import ArticleUploadForm

from parsifal.utils.elsevier.client import ElsevierClient
from parsifal.utils.elsevier.exceptions import *


@author_required
@login_required
def conducting(request, username, review_name):
    return redirect(r('search_studies', args=(username, review_name)))

@author_required
@login_required
def search_studies(request, username, review_name):
    review = get_object_or_404(Review, name=review_name, author__username__iexact=username)
    sessions = review.get_latest_source_search_strings()
    add_sources = review.sources.exclude(id__in=sessions.values('source__id'))
    database_queries = {}
    try:
        scopus = sessions.filter(source__name__iexact='Scopus')[0]
        database_queries['scopus'] = scopus
    except:
        pass
    try:
        science_direct = sessions.filter(source__name__iexact='Science@Direct')[0]
        database_queries['science_direct'] = science_direct
    except:
        pass
    sources_names = []
    for source in review.sources.all():
        sources_names.append(source.name.lower())
    return render(request, 'conducting/conducting_search_studies.html', { 
            'review': review, 
            'add_sources': add_sources,
            'database_queries': database_queries,
            'sources_names': sources_names
            })

@author_required
@login_required
@require_POST
def save_source_string(request):
    try:
        review_id = request.POST.get('review-id')
        source_id = request.POST.get('source-id')
        review = Review.objects.get(pk=review_id)
        source = Source.objects.get(pk=source_id)
        search_string = request.POST.get('search_string')
        try:
            search_session = review.get_latest_source_search_strings().get(source=source)
        except SearchSession.DoesNotExist:
            search_session = SearchSession(review=review, source=source)
        search_session.search_string = search_string
        search_session.save()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()

@author_required
@login_required
@require_POST
def remove_source_string(request):
    try:
        review_id = request.POST.get('review-id')
        source_id = request.POST.get('source-id')
        review = Review.objects.get(pk=review_id)
        source = Source.objects.get(pk=source_id)
        search_string = request.POST.get('search_string')
        try:
            search_session = review.get_latest_source_search_strings().get(source=source)
            search_session.delete()
        except SearchSession.DoesNotExist:
            pass
        messages.success(request, u'{0} search string removed successfully!'.format(source.name))
    except:
        messages.error(request, u'{0} search string removed successfully!'.format(source.name))
    return redirect(r('search_studies', args=(review.author.username, review.name)))

@author_required
@login_required
@require_POST
def import_base_string(request):
    try:
        review_id = request.POST.get('review-id')
        source_id = request.POST.get('source-id')
        review = Review.objects.get(pk=review_id)
        source = Source.objects.get(pk=source_id)
        base_search_string = review.get_generic_search_string().search_string
        try:
            search_session = review.get_latest_source_search_strings().get(source=source)
        except SearchSession.DoesNotExist:
            search_session = SearchSession(review=review, source=source)
        search_session.search_string = base_search_string
        search_session.save()
        return HttpResponse(base_search_string)
    except:
        return HttpResponseBadRequest()

def elsevier_search(request, database):
    client = ElsevierClient(django_settings.ELSEVIER_API_KEY)
    query = request.GET.get('query', '')
    query = ' '.join(query.split())
    count = request.GET.get('count', '25')
    start = request.GET.get('start', '0')
    print count
    print start
    try:
        result = {}
        if database == 'scopus':
            result = client.search_scopus({ 'query': query, 'count': count, 'start': start })
        elif database == 'science_direct':
            result = client.search_science_direct({ 'query': query, 'count': count, 'start': start })
        data = json.dumps(result)
        return HttpResponse(data, content_type='application/json')
    except ElsevierInvalidRequest, e:
        return HttpResponseBadRequest('Invalid query. Please verify the syntax of your query before executing a new search.')
    except ElsevierQuotaExceeded, e:
        return HttpResponseBadRequest('Parsifal\'s search quota on Elsevier\'s databases exceeded. Please try again later.')


@author_required
@login_required
def search_scopus(request):
    return elsevier_search(request, 'scopus')

@author_required
@login_required
def search_science_direct(request):
    return elsevier_search(request, 'science_direct')

@author_required
@login_required
def import_studies(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username__iexact=username)
    sources = []
    for source in review.sources.all():
        sources.append({
            'source': source, 
            'count': Article.objects.filter(source=source, review=review).count()
            })
    context = RequestContext(request, { 'review': review, 'sources': sources })
    return render_to_response('conducting/conducting_import_studies.html', context)

@author_required
@login_required
def study_selection(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username__iexact=username)
    try:
        active_tab = int(request.GET['source'])
    except Exception, e:
        active_tab = -1

    add_sources = review.sources.count()
    import_articles = review.get_source_articles().count()

    steps_messages = []

    if not add_sources: steps_messages.append('Use the <a href="/'+ username +'/'+ review_name +'/planning/">planning tab</a> to add sources to your review.')
    if not import_articles: steps_messages.append('Import the studies using the <a href="/'+ username +'/'+ review_name +'/conducting/import/">import studies tab</a>.')

    finished_all_steps = len(steps_messages) == 0

    context = RequestContext(request, {'review': review, 'active_tab': active_tab, 'steps_messages': steps_messages, 'finished_all_steps': finished_all_steps})
    return render_to_response('conducting/conducting_study_selection.html', context)

def get_workflow_steps(self, review):
    pass

def build_quality_assessment_table(request, review):
    selected_studies = review.get_accepted_articles()
    quality_questions = review.get_quality_assessment_questions()
    quality_answers = review.get_quality_assessment_answers()

    if quality_questions and quality_answers:   
        str_table = u'' 
        for study in selected_studies:
            str_table += u'''
            <div class="panel panel-default">
              <div class="panel-heading">
                <h3 class="panel-title">{0}<span class="badge score pull-right">{1}</span></h3>
              </div>

            <table class="table" id="tbl-quality" article-id="{2}" csrf-token="{3}">
                <tbody>'''.format(study.title, study.get_score(), study.id, unicode(csrf(request)['csrf_token']))

            quality_assessment = study.get_quality_assesment()

            for question in quality_questions:
                str_table += u'''<tr question-id="''' + str(question.id) + '''">
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
                    str_table += u'''<td class="answer'''+ selected_answer +'''" answer-id="''' + str(answer.id) + '''">''' + answer.description + '''</td>'''
                str_table += u'''</tr>'''

            str_table += u'''</tbody></table></div>'''
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
    if not import_articles: steps_messages.append('Import the studies using the <a href="/'+ username +'/'+ review_name +'/conducting/import/">import studies tab</a>.')
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

        str_field = u'''<select name="value" class="form-control">
            <option value="">Select...</option>
            <option value="True"{0}>True</option>
            <option value="False"{1}>False</option>
          </select>'''.format(true, false)

    elif field.field_type == field.DATE_FIELD:
        if extraction != None:
            value = extraction.get_date_value_as_string()
        else:
            value = u''
        str_field = u'<input type="text" class="form-control" name="{0}-{1}-value" maxlength="10" value="{2}">'.format(article.id, field.id, value)

    elif field.field_type == field.SELECT_ONE_FIELD:
        str_field = u'''<select name="{0}-{1}-value" class="form-control">
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
            str_field += u'<label class="checkbox-inline"><input type="checkbox" name="{0}-{1}-value" value="{2}"{3}>{4}</label> '.format(article.id, field.id, value.id, checked, value.value)

    else:
        if extraction != None:
            value = extraction.get_value()
        else:
            value = u''
        str_field = u'<input type="text" class="form-control" name="{0}-{1}-value" maxlength="1000" value="{2}">'.format(article.id, field.id, value)

    return str_field

def build_data_extraction_table(review):
    selected_studies = review.get_final_selection_articles()
    data_extraction_fields = review.get_data_extraction_fields()
    if data_extraction_fields:
        str_table = u'<div class="panel-group">'
        for study in selected_studies:
            str_table += u'''<div class="panel panel-success data-extraction-panel">
              <div class="panel-heading">
                <h3 class="panel-title">{1} <span class="badge pull-right">{2}</span></h3>
              </div>
              <div class="panel-body form-horizontal" data-article-id="{0}">'''.format(study.id, study.title, study.get_score())
            for field in data_extraction_fields:
                str_table += u'''<div class="form-group" data-field-id="{0}">
                    <label class="control-label col-md-2">{1}</label>
                    <div class="col-md-10">{2}<span class="help-block error" style="display: none;"></span>
                    </div>
                </div>
                '''.format(field.id, field.description, build_data_extraction_field_row(study, field))
            str_table += u'</div></div>'
        str_table += "</div>"
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
    if not import_articles: steps_messages.append('Import the studies using the <a href="/'+ username +'/'+ review_name +'/conducting/import/">import studies tab</a>.')
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

def bibtex_to_article_object(filename, review, source):
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
            article.review = review
            article.source = source
        except:
            continue
        articles.append(article)
    return articles

@author_required
@login_required
@require_POST
def import_bibtex(request):
    review_id = request.POST['review-id']
    source_id = request.POST['source-id']

    review = Review.objects.get(pk=review_id)
    source = Source.objects.get(pk=source_id)

    f = request.FILES['bibtex']
    filename = django_settings.FILE_UPLOAD_TEMP_DIR + request.user.username + '.bib'
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    articles = bibtex_to_article_object(filename, review, source)
    if any(articles):
        for article in articles:
            article.save()
        messages.success(request, u'{0} articles successfully imported to {1}!'.format(len(articles), source.name))
    return redirect(r('import_studies', args=(review.author.username, review.name)))

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


@author_required
@login_required
def article_details(request):
    article_id = request.GET['article-id']
    article = Article.objects.get(pk=article_id)
    upload_form = ArticleUploadForm()
    user = request.user
    mendeley_files = []
    if user.profile.mendeley_token:
        mendeley_files = user.profile.get_mendeley_session().files.list().items
    context = RequestContext(request, { 'article': article, 'upload_form': upload_form, 'mendeley_files': mendeley_files })
    return render_to_response('conducting/partial_conducting_article_details.html', context)

@author_required
@login_required
def articles_upload(request):
    if request.method == 'POST':
        form = ArticleUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['article_file']
            review_id = request.POST.get('review-id')
            review = Review.objects.get(pk=review_id)

            article_id = request.POST.get('article-id')
            article = Article.objects.get(pk=article_id)

            article_file = ArticleFile(review=review, 
                    article=article, 
                    user=request.user, 
                    article_file=uploaded_file,
                    name=uploaded_file.name,
                    size=uploaded_file.size)
            article_file.save()

            results = [ { 'name': article_file.name, 'size': article_file.size } ]

            return HttpResponse(json.dumps(results), content_type='application/json')
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

def build_article_table_row(article):
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
            article.get_status_html())
    return row


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


@author_required
@login_required
def find_duplicates(request):
    review_id = request.GET['review-id']
    review = Review.objects.get(pk=review_id)
    duplicates = review.get_duplicate_articles()
    context = RequestContext(request, {'duplicates': duplicates})
    return render_to_response('conducting/partial_conducting_find_duplicates.html', context)


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

@author_required
@login_required
def data_analysis(request, username, review_name):
    review = get_object_or_404(Review, name=review_name, author__username__iexact=username)
    return render(request, 'conducting/conducting_data_analysis.html', { 'review': review })

def articles_selection_chart(request):
    review_id = request.GET['review-id']
    review = Review.objects.get(pk=review_id)
    selected_articles = review.get_accepted_articles()
    articles = []
    for source in review.sources.all():
        count = review.get_source_articles(source.id).count()
        accepted_count = selected_articles.filter(source__id=source.id).count()
        articles.append(source.name + ':' + str(count) + ':' + str(accepted_count))
    return HttpResponse(','.join(articles))

def articles_per_year(request):
    review_id = request.GET['review-id']
    review = Review.objects.get(pk=review_id)
    final_articles = review.get_final_selection_articles().values('year').annotate(count=Count('year')).order_by('-year')
    articles = []
    for article in final_articles:
        articles.append(article['year'] + ':' + str(article['count']))
    return HttpResponse(','.join(articles))

@author_required
@login_required
@require_POST
def add_source_string(request):
    review_id = request.POST.get('review-id')
    review = get_object_or_404(Review, pk=review_id)
    source_ids = request.POST.getlist('source')
    for source_id in source_ids:
        try:
            source = Source.objects.get(pk=source_id)
            exists = SearchSession.objects.filter(review=review, source=source).exists()
            if not exists:
                search_session = SearchSession(review=review, source=source)
                search_session.save()
        except Source.DoesNotExist:
            pass
    review.save()
    messages.success(request, 'Sources search string successfully added to the review!')
    return redirect(r('search_studies', args=(review.author.username, review.name)))
