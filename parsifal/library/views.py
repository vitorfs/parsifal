import json
import os
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse as r
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from reviews.models import Review, Article
from parsifal.library.models import Folder, Document
from parsifal.library.forms import FolderForm, DocumentForm


def get_paginated_documents(request, queryset):
    paginator = Paginator(queryset, 25)
    page = request.GET.get('page')
    try:
        documents = paginator.page(page)
    except PageNotAnInteger:
        documents = paginator.page(1)
    except EmptyPage:
        documents = paginator.page(paginator.num_pages)
    return documents

def library(request, documents, querystring, active_folder=None):
    reviews = Review.objects.filter(author=request.user)
    folder_form = FolderForm()
    current_full_path = request.get_full_path()
    return render(request, 'library/library.html', { 
            'reviews': reviews, 
            'documents': documents,
            'querystring': querystring,
            'active_folder': active_folder,
            'folder_form': folder_form,
            'current_full_path': current_full_path
        })

@login_required
def index(request):
    querystring = request.GET.get('q', '')
    queryset = Document.objects.filter(user=request.user)
    if querystring:
        queryset = queryset.filter(title__icontains=querystring)
    documents = get_paginated_documents(request, queryset)
    return library(request, documents, querystring)

@login_required
def folder(request, slug):
    querystring = request.GET.get('q', '')
    folder = get_object_or_404(Folder, slug=slug)
    queryset = folder.documents.all()
    if querystring:
        queryset = queryset.filter(title__icontains=querystring)
    documents = get_paginated_documents(request, queryset)
    return library(request, documents, querystring, folder)

def save_folder(form):
    base_slug = slugify(form.instance.name)
    unique_slug = base_slug
    i = 0
    while Folder.objects.filter(slug=unique_slug):
        i = i + 1
        unique_slug = u'{0}-{1}'.format(base_slug, i)
    form.instance.slug = unique_slug
    folder = form.save()
    return folder

@login_required
@require_POST
def new_folder(request):
    form = FolderForm(request.POST)
    if form.is_valid():
        form.instance.user = request.user
        folder = save_folder(form)
        dump = json.dumps({ 'folder': { 'id': folder.id, 'name': folder.name, 'slug': folder.slug } })
        return HttpResponse(dump, content_type='application/json')
    else:
        dump = json.dumps(form.errors)
        return HttpResponseBadRequest(dump, content_type='application/json')

@login_required
@require_POST
def edit_folder(request):
    deleteFolder = request.POST.get('delete', '') == 'delete'
    folder_id = request.POST.get('id')
    folder = Folder.objects.get(pk=folder_id)
    if deleteFolder:
        folder.delete()
        messages.success(request, u'The folder {0} was deleted successfully!'.format(folder.name))
        return redirect(r('library:index'))
    else:    
        form = FolderForm(request.POST, instance=folder)
        if form.is_valid():
            form.instance.user = request.user
            folder = save_folder(form)
            messages.success(request, u'The folder {0} was changed successfully!'.format(folder.name))
        else:
            messages.error(request, u'An error ocurred while trying to save folder {0}'.format(folder.name))
    return redirect(r('library:folder', args=(folder.slug,)))

@login_required
def document(request, document_id):
    document = Document.objects.get(pk=document_id)
    json_context = {}
    if request.method == 'POST':
        form = DocumentForm(request.POST, instance=document)
        if form.is_valid():
            document = form.save()
            json_context['status'] = 'success'
            json_context['html'] = render_to_string('library/partial_document_summary.html', { 'document': document })
            return HttpResponse(json.dumps(json_context), content_type='application/json')
        else:
            json_context['status'] = 'error'
    else:
        form = DocumentForm(instance=document)
        json_context['status'] = 'ok'
    csrf_token = unicode(csrf(request)['csrf_token'])
    json_context['html'] = render_to_string('library/document.html', { 'form': form, 'csrf_token': csrf_token })
    return HttpResponse(json.dumps(json_context), content_type='application/json')

@login_required
def new_document(request):
    json_context = {}
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            document = form.save()
            messages.success(request, 'Document added successfully!')
            json_context['status'] = 'success'
            json_context['redirect_to'] = r('library:index')
        else:
            json_context['status'] = 'error'
    else:
        form = DocumentForm()
        json_context['status'] = 'ok'
    csrf_token = unicode(csrf(request)['csrf_token'])
    html = render_to_string('library/new_document.html', { 'form': form, 'csrf_token': csrf_token })
    json_context['html'] = html
    dump = json.dumps(json_context)
    return HttpResponse(dump, content_type='application/json')

def get_document_verbose_name(documents_size):
    document_verbose_name = 'document'
    if documents_size > 1:
        document_verbose_name = 'documents'
    return document_verbose_name

@login_required
@require_POST
def move(request):
    move_from_folder_id = request.POST.get('move_from')
    move_from_folder = Folder.objects.get(pk=move_from_folder_id)

    move_to_folder_id = request.POST.get('move_to')
    move_to_folder = Folder.objects.get(pk=move_to_folder_id)

    documents = request.POST.getlist('document')

    documents_feedback = {}
    documents_feedback['success'] = 0
    documents_feedback['warning'] = 0

    document_list = []
    for document in documents:
        try:
            move_to_folder.documents.add(document)
            move_from_folder.documents.remove(document)
            documents_feedback['success'] += 1
            document_list.append(document)
        except:
            documents_feedback['warning'] += 1

    success_message = ''
    if documents_feedback['success'] > 0:
        success_message = u'{0} {1} moved from folder {2} to {3}!'.format(
                documents_feedback['success'], 
                get_document_verbose_name(documents_feedback['success']), 
                move_from_folder.name,
                move_to_folder.name
                )

    warning_message = ''
    if documents_feedback['warning'] > 0:
        warning_message = u'{0} {1} couldn\'t be moved because they were already in folder {2}'.format(
                documents_feedback['warning'], 
                get_document_verbose_name(documents_feedback['warning']),
                move_to_folder.name
                )

    return HttpResponse(json.dumps({ 
            'documents': document_list,
            'success_message': success_message, 
            'warning_message': warning_message 
        }), content_type='application/json')

@login_required
@require_POST
def copy(request):
    copy_to_folder_id = request.POST.get('copy_to')
    copy_to_folder = Folder.objects.get(pk=copy_to_folder_id)
    documents = request.POST.getlist('document')

    documents_feedback = {}
    documents_feedback['success'] = 0
    documents_feedback['warning'] = 0

    for document in documents:
        try:
            copy_to_folder.documents.add(document)
            documents_feedback['success'] += 1
        except:
            documents_feedback['warning'] += 1

    success_message = ''
    if documents_feedback['success'] > 0:
        success_message = u'{0} {1} successfully copied to folder {2}!'.format(
                documents_feedback['success'], 
                get_document_verbose_name(documents_feedback['success']), 
                copy_to_folder.name
                )

    warning_message = ''
    if documents_feedback['warning'] > 0:
        warning_message = u'{0} {1} couldn\'t be copied because they were already in folder {2}'.format(
                documents_feedback['warning'], 
                get_document_verbose_name(documents_feedback['warning']),
                copy_to_folder.name
                )

    return HttpResponse(json.dumps({ 'success_message': success_message, 'warning_message': warning_message }), content_type='application/json')

@login_required
@require_POST
def remove_from_folder(request):
    remove_from_folder_id = request.POST.get('remove_from')
    folder = Folder.objects.get(pk=remove_from_folder_id)
    documents = request.POST.getlist('document')
    folder.documents.remove(*documents)
    documents_size = len(documents)
    message = u'{0} {1} successfully removed from folder {2}!'.format(
            documents_size, 
            get_document_verbose_name(documents_size), 
            folder.name)
    return HttpResponse(json.dumps({ 'documents': documents, 'message': message }), content_type='application/json')

@login_required
@require_POST
def delete_documents(request):
    document_ids = request.POST.getlist('document')
    documents = Document.objects.filter(id__in=document_ids)
    documents_size = documents.count()
    documents.delete()
    message = u'{0} {1} successfully deleted!'.format(documents_size, get_document_verbose_name(documents_size))
    return HttpResponse(json.dumps({ 'documents': document_ids, 'message': message }), content_type='application/json')

@login_required
@require_POST
def import_bibtex(request):
    redirect_to = request.POST.get('redirect', r('library:index'))
    bibtex_file = request.FILES['bibtex']

    ext = os.path.splitext(bibtex_file.name)[1]
    valid_extensions = ['.bib', '.bibtex']

    if ext in valid_extensions or bibtex_file.content_type == 'application/x-bibtex':
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        bib_database = bibtexparser.load(bibtex_file, parser=parser)

        documents = []
        with transaction.atomic():
            for entry in bib_database.entries:
                document = Document(user=request.user)
                document.bibtexkey = entry.get('id', None)
                document.address = entry.get('address', entry.get('correspondence_address1', None))
                document.author = entry.get('authors', entry.get('author', None))
                document.booktitle = entry.get('booktitle', None)
                document.chapter = entry.get('chapter', None)
                document.crossref = entry.get('crossref', None)
                document.edition = entry.get('edition', None)
                document.editor = entry.get('editor', None)
                document.howpublished = entry.get('howpublished', None)
                document.institution = entry.get('institution', None)
                document.journal = entry.get('journal', None)
                document.month = entry.get('month', None)
                document.note = entry.get('note', None)
                document.number = entry.get('number', None)
                document.organization = entry.get('organization', None)
                document.pages = entry.get('pages', None)
                document.publisher = entry.get('publisher', None)
                document.school = entry.get('school', None)
                document.series = entry.get('series', None)
                document.title = entry.get('title', None)
                document.publication_type = entry.get('type', entry.get('publication_type', None))
                document.volume = entry.get('volume', None)
                document.year = entry.get('year', None)
                document.abstract = entry.get('abstract', None)
                document.coden = entry.get('coden', None)
                document.doi = entry.get('doi', None)
                document.isbn = entry.get('isbn', None)
                document.issn = entry.get('issn', None)
                document.keywords = entry.get('author_keywords', entry.get('keywords', None))
                document.language = entry.get('language', None)
                document.url = entry.get('url', entry.get('link', None))
                document.save()
                documents.append(document)

        if any(documents):
            messages.success(request, u'{0} documents imported!'.format(len(documents)))
        else:
            messages.warning(request, u'The bibtex file had no valid entry!')
    else:
        messages.error(request, u'Invalid file type. Only .bib or .bibtex files are accepted.')

    return redirect(redirect_to)
