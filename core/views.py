# coding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from reviews.models import Review
from activities.models import Activity
from django.db.models import Q
from datetime import datetime

def get_following_feeds(user):
    feeds = []    
    try:
        activities = []
        followers = Activity.objects.filter(to_user=user, activity_type=Activity.FOLLOW)
        for follower_user in followers:
            activities.append(follower_user)
        following = Activity.objects.filter(from_user=user, activity_type=Activity.FOLLOW)
        for following_user in following:
            activities.append(following_user)
            initial_activity = Activity.objects.get(from_user=user, to_user=following_user.to_user, activity_type=Activity.FOLLOW)
            following_user_activities = Activity.objects.filter(from_user=following_user.to_user, activity_type=Activity.FOLLOW, date__gte=initial_activity.date).exclude(to_user=user)
            for activity in following_user_activities:
                activities.append(activity)
        activities.sort(key=lambda a: a.date, reverse=True)
        for activity in activities:
            if activity.from_user == user:
                activity.message = u'<a href="/{0}/">You</a> are now following <a href="/{1}/">{2}</a>'.format(
                    user.username,
                    activity.to_user.username,
                    activity.to_user.profile.get_screen_name())
            else:
                is_following = activity.to_user.profile.get_screen_name()
                if activity.to_user == user:
                    is_following = u'you'
                activity.message = u'<a href="/{0}/">{1}</a> is now following <a href="/{2}/">{3}</a>'.format(
                    activity.from_user.username,
                    activity.from_user.profile.get_screen_name(), 
                    activity.to_user.username,
                    is_following)
            feeds.append(activity)
    except Exception, e:
        pass
    return feeds

def home(request):
    if request.user.is_authenticated():
        user_reviews = Review.objects.filter(Q(author=request.user) | Q(co_authors=request.user)).order_by('-last_update',)
        feeds = get_following_feeds(request.user)
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