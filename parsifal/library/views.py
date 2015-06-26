import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse as r
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.views.decorators.http import require_POST

from reviews.models import Review, Article
from parsifal.library.models import Folder, Document
from parsifal.library.forms import FolderForm


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

def library(request, documents, active_folder=None):
    reviews = Review.objects.filter(author=request.user)
    folder_form = FolderForm()
    return render(request, 'library/library.html', { 
            'reviews': reviews, 
            'documents': documents, 
            'active_folder': active_folder,
            'folder_form': folder_form
        })

@login_required
def index(request):
    queryset = Article.objects.filter(review__author=request.user)
    documents = get_paginated_documents(request, queryset)
    return library(request, documents)

@login_required
def folder(request, slug):
    folder = get_object_or_404(Folder, slug=slug)
    queryset = Document.objects.filter(user=request.user)
    documents = get_paginated_documents(request, queryset)
    return library(request, documents, folder)

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
