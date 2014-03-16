# coding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from reviews.models import Review

def home(request):
    if request.user.is_authenticated():
        user_reviews = Review.objects.filter(author__id=request.user.id).order_by('-last_update',)
        context = RequestContext(request, {'user_reviews': user_reviews})
        return render_to_response('core/home.html', context)
    else:
        context = RequestContext(request)
        return render_to_response('core/cover.html', context)

def about(request):
    context = RequestContext(request)
    return render_to_response('core/about.html', context)

def help(request):
    context = RequestContext(request)
    return render_to_response('core/help.html', context)

def support(request):
    context = RequestContext(request)
    return render_to_response('core/support.html', context)

def explore(request):
    context = RequestContext(request)
    return render_to_response('core/explore.html', context)