from django.shortcuts import render_to_response
from django.template import RequestContext

def entries(request):
    context = RequestContext(request)
    return render_to_response('blog/entries.html', context)