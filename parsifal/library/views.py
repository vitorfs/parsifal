import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
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

def library(request, documents, active_folder):
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
    return library(request, documents, 'all')

@login_required
def folder(request, slug):
    folder = Folder.objects.get(slug=slug)
    queryset = Document.objects.filter(user=request.user)
    documents = get_paginated_documents(request, queryset)
    return library(request, documents, slug)

@login_required
@require_POST
def new_folder(request):
    form = FolderForm(request.POST)
    if form.is_valid():
        form.instance.user = request.user
        form.instance.slug = slugify(form.instance.name)
        folder = form.save()
        dump = json.dumps({ 'folder': { 'id': folder.id, 'name': folder.name, 'slug': folder.slug } })
        return HttpResponse(dump, content_type='application/json')
    else:
        dump = json.dumps(form.errors)
        return HttpResponseBadRequest(dump, content_type='application/json')
