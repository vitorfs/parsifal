from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from blog.models import Entry

def entries(request):
    entries = Entry.objects.filter(status='PUBLISHED').order_by('-start_publication',)
    context = RequestContext(request, {'entries': entries})
    return render_to_response('blog/entries.html', context)

def entry(request, slug):
    try:
        blog_entry = Entry.objects.get(slug=slug, status='PUBLISHED')
    except Entry.DoesNotExist:
        raise Http404
    context = RequestContext(request, {'entry': blog_entry})
    return render_to_response('blog/entry.html', context)