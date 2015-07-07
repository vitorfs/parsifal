from django.shortcuts import render, get_object_or_404
from parsifal.blog.models import Entry

def entries(request):
    entries = Entry.objects.filter(status=Entry.PUBLISHED).order_by('-start_publication',)
    return render(request, 'blog/entries.html', { 'entries': entries })

def entry(request, slug):
    blog_entry = get_object_or_404(Entry, slug=slug, status=Entry.PUBLISHED)
    return render(request, 'blog/entry.html', { 'entry': blog_entry })
    