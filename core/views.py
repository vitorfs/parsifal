# coding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from reviews.models import Review
from activities.models import Activity
from django.db.models import Q
import datetime

def home(request):
    if request.user.is_authenticated():
        user_reviews = Review.objects.filter(Q(author=request.user) | Q(co_authors=request.user)).order_by('-last_update',)
        followers = request.user.profile.get_following()
        feeds = []
        activities = []

        for follower in followers:
            follower_activities = Activity.objects.filter(from_user__pk=follower.pk, activity_type=Activity.FOLLOW)
            for activity in follower_activities:
                activities.append(activity)
        
        activities.sort(key=lambda a: a.date, reverse=True)

        for activity in activities:
            is_following = activity.to_user.profile.get_screen_name()
            if activity.to_user == request.user:
                is_following = 'you'
            feeds.append('{0} - <a href="/{1}/">{2}</a> is now following <a href="/{3}/">{4}</a>.'.format(
                activity.date.strftime('%m/%d/%Y'),
                activity.from_user.username,
                activity.from_user.profile.get_screen_name(), 
                activity.to_user.username,
                is_following)
            )
        context = RequestContext(request, {'user_reviews': user_reviews, 'feeds': feeds, })
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