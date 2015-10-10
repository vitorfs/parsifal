# coding: utf-8

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
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from parsifal.reviews.models import Review, Article
from parsifal.library.models import Folder, Document
from parsifal.library.forms import FolderForm, DocumentForm, SharedFolderForm


def get_order(request):
    order = request.GET.get('o', '').lower()
    if order in ['title', '-title', 'author', '-author', 'year', '-year']:
        return order
    return 'title'

def get_paginated_documents(request, queryset):
    paginator = Paginator(queryset, 100)
    page = request.GET.get('p')
    try:
        documents = paginator.page(page)
    except PageNotAnInteger:
        documents = paginator.page(1)
    except EmptyPage:
        documents = paginator.page(paginator.num_pages)
    return documents

def get_filtered_documents(queryset, querystring):
    if querystring:
        queryset = queryset.filter(title__icontains=querystring)
    return queryset

def library(request, documents, querystring, order, active_folder=None):
    reviews = Review.objects.filter(author=request.user)
    folder_form = FolderForm(initial={ 'user': request.user })
    shared_folder_form = SharedFolderForm()
    current_full_path = request.get_full_path()
    return render(request, 'library/library.html', { 
            'reviews': reviews, 
            'documents': documents,
            'querystring': querystring,
            'order': order,
            'active_folder': active_folder,
            'folder_form': folder_form,
            'shared_folder_form': shared_folder_form,
            'current_full_path': current_full_path
        })

@login_required
def index(request):
    querystring = request.GET.get('q', '')
    order = get_order(request)
    queryset = Document.objects.filter(user=request.user)
    queryset = get_filtered_documents(queryset, querystring)
    queryset = queryset.order_by(order)
    documents = get_paginated_documents(request, queryset)
    return library(request, documents, querystring, order)

@login_required
@require_POST
def list_actions(request):
    action = request.POST.get('action')
    if action == 'remove_from_folder':
        return remove_from_folder(request)
    elif action == 'delete_documents':
        return delete_documents(request)
    elif action == 'move':
        return move(request)
    elif action == 'copy':
        return copy(request)
    redirect_to = request.POST.get('redirect', r('library:index'))
    return redirect(redirect_to)

@login_required
def folder(request, slug):
    querystring = request.GET.get('q', '')
    order = get_order(request)
    folder = get_object_or_404(Folder, slug=slug)
    queryset = folder.documents.all()
    queryset = get_filtered_documents(queryset, querystring)
    queryset = queryset.order_by(order)
    documents = get_paginated_documents(request, queryset)
    return library(request, documents, querystring, order, folder)

@login_required
@require_POST
def new_folder(request):
    form = FolderForm(request.POST)
    if form.is_valid():
        form.instance.user = request.user
        folder = form.save()
        dump = json.dumps({ 'folder': { 'id': folder.id, 'name': folder.name, 'slug': folder.slug } })
        return HttpResponse(dump, content_type='application/json')
    else:
        dump = json.dumps(form.errors)
        return HttpResponseBadRequest(dump, content_type='application/json')

@login_required
@require_POST
def edit_folder(request):
    delete_folder = request.POST.get('delete', '') == 'delete'
    folder_id = request.POST.get('id')
    folder = Folder.objects.get(pk=folder_id)
    if delete_folder:
        folder.delete()
        messages.success(request, u'The folder {0} was deleted successfully!'.format(folder.name))
        return redirect(r('library:index'))
    else:    
        form = FolderForm(request.POST, instance=folder)
        if form.is_valid():
            form.instance.user = request.user
            folder = form.save()
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
    move_from_folder_id = request.POST.get('active-folder-id')
    move_from_folder = Folder.objects.get(pk=move_from_folder_id)

    move_to_folder_id = request.POST.get('action-folder-id')
    move_to_folder = Folder.objects.get(pk=move_to_folder_id)

    if request.POST.get('select-all-pages') == 'all':
        documents = move_from_folder.documents.all()
    else:
        document_ids = request.POST.getlist('document')
        documents = Document.objects.filter(id__in=document_ids)

    querystring = request.POST.get('querystring', '')
    documents = get_filtered_documents(documents, querystring)

    move_to_folder.documents.add(*documents)
    move_from_folder.documents.remove(*documents)

    messages.success(request, u'Documents moved from folder {0} to {1} successfully!'.format(move_from_folder.name, move_to_folder.name))
    redirect_to = request.POST.get('redirect', r('library:index'))
    return redirect(redirect_to)

@login_required
@require_POST
def copy(request):
    redirect_to = request.POST.get('redirect', r('library:index'))

    copy_from_folder_id = request.POST.get('active-folder-id')
    copy_to_folder_id = request.POST.get('action-folder-id')

    try:
        copy_to_folder = Folder.objects.get(pk=copy_to_folder_id)
    except Folder.DoesNotExist:
        messages.error(u'The folder you are trying to copy does not exist.')
        return redirect(redirect_to)

    select_all_pages = request.POST.get('select-all-pages')
    document_ids = request.POST.getlist('document')

    if copy_from_folder_id:
        try:
            copy_from_folder = Folder.objects.get(pk=copy_from_folder_id)
            documents = copy_from_folder.documents.all()
        except Folder.DoesNotExist:
            messages.error(u'The folder you are trying to copy does not exist.')
            return redirect(redirect_to)
    else:
        documents = Document.objects.filter(user=request.user)

    if select_all_pages == 'all':
        querystring = request.POST.get('querystring', '')
        documents = get_filtered_documents(documents, querystring)
    else:
        documents = documents.filter(id__in=document_ids)

    copy_to_folder.documents.add(*documents)
    messages.success(request, u'Documents copied to folder {0} successfully!'.format(copy_to_folder.name))
    return redirect(redirect_to)

@login_required
@require_POST
def remove_from_folder(request):
    remove_from_folder_id = request.POST.get('active-folder-id')
    folder = Folder.objects.get(pk=remove_from_folder_id)
    select_all_pages = request.POST.get('select-all-pages')

    if select_all_pages == 'all':
        querystring = request.POST.get('querystring', '')
        documents = folder.documents.all()
        documents = get_filtered_documents(documents, querystring)
        documents_size = documents.count()
        folder.documents.remove(*documents)
    else:
        documents = request.POST.getlist('document')
        documents_size = len(documents)
        folder.documents.remove(*documents)

    messages.success(request, u'{0} {1} successfully removed from folder {2}!'.format(
            documents_size, 
            get_document_verbose_name(documents_size), 
            folder.name)
        )
    redirect_to = request.POST.get('redirect', r('library:index'))
    return redirect(redirect_to)

@login_required
@require_POST
def delete_documents(request):
    select_all_pages = request.POST.get('select-all-pages')
    document_ids = request.POST.getlist('document')
    folder_id = request.POST.get('active-folder-id')

    if folder_id:
        folder = Folder.objects.get(pk=folder_id)
        if select_all_pages == 'all':
            documents = folder.documents.all()
        else:
            documents = folder.documents.filter(id__in=document_ids)
    else:
        if select_all_pages == 'all':
            documents = Document.objects.filter(user=request.user)
        else:
            documents = Document.objects.filter(user=request.user, id__in=document_ids)

    querystring = request.POST.get('querystring', '')
    documents = get_filtered_documents(documents, querystring)
        
    documents_size = documents.count()
    documents.delete()
    messages.success(request, u'{0} {1} successfully deleted!'.format(
            documents_size, 
            get_document_verbose_name(documents_size))
        )
    redirect_to = request.POST.get('redirect', r('library:index'))
    return redirect(redirect_to)

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
                document.entry_type = entry.get('type', None)
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
                document.publication_type = entry.get('document_type', entry.get('publication_type', None))
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
            folder_id = request.POST.get('add-to-folder-id')
            if folder_id:
                try:
                    folder = Folder.objects.get(pk=folder_id)
                    folder.documents.add(*documents)
                except Folder.DoesNotExist:
                    messages.error(request, u'Folder does not exists.')
            messages.success(request, u'{0} documents imported!'.format(len(documents)))
        else:
            messages.warning(request, u'The bibtex file had no valid entry!')
    else:
        messages.error(request, u'Invalid file type. Only .bib or .bibtex files are accepted.')

    return redirect(redirect_to)

@login_required
def shared_folder(request, slug):
    querystring = request.GET.get('q', '')
    order = get_order(request)
    shared_folder = get_object_or_404(SharedFolder, slug=slug)
    queryset = shared_folder.documents.all()
    queryset = get_filtered_documents(queryset, querystring)
    queryset = queryset.order_by(order)
    documents = get_paginated_documents(request, queryset)
    return library(request, documents, querystring, order, shared_folder)

@login_required
@require_POST
def new_shared_folder(request):
    form = SharedFolderForm(request.POST)
    if form.is_valid():
        folder = form.save()
        dump = json.dumps({ 'folder': { 'id': folder.id, 'name': folder.name, 'slug': folder.slug } })
        return HttpResponse(dump, content_type='application/json')
    else:
        dump = json.dumps(form.errors)
        return HttpResponseBadRequest(dump, content_type='application/json')
