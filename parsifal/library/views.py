import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse as r
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.core.context_processors import csrf
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
    return render(request, 'library/library.html', { 
            'reviews': reviews, 
            'documents': documents,
            'querystring': querystring,
            'active_folder': active_folder,
            'folder_form': folder_form
        })

@login_required
def index(request):
    querystring = request.GET.get('q', '')
    queryset = Article.objects.filter(review__author=request.user)
    if querystring:
        queryset = queryset.filter(title__icontains=querystring)
    documents = get_paginated_documents(request, queryset)
    return library(request, documents, querystring)

@login_required
def folder(request, slug):
    querystring = request.GET.get('q', '')
    folder = get_object_or_404(Folder, slug=slug)
    queryset = Document.objects.filter(user=request.user)
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
def document(request, slug):
    pass

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
