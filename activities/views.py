from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from activities.models import Activity
from django.contrib.auth.models import User

def follow(request, username):
    from_user = request.user
    to_user = get_object_or_404(User, username=username)
    followers = from_user.profile.get_followers()
    if to_user not in followers:
        activity = Activity(from_user=from_user, to_user=to_user, activity_type=Activity.FOLLOW)
        activity.save()
    return HttpResponseRedirect('/' + username + '/' )

def unfollow(request, username):
    return HttpResponseRedirect('/')