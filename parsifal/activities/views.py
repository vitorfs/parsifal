from django.template import RequestContext
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from parsifal.activities.models import Activity


@login_required
def follow(request):
    try:
        user_id = request.GET['user-id']
        to_user = get_object_or_404(User, pk=user_id)
        from_user = request.user

        following = from_user.profile.get_following()

        if to_user not in following:
            activity = Activity(from_user=from_user, to_user=to_user, activity_type=Activity.FOLLOW)
            activity.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
    except:
        return HttpResponseBadRequest()


@login_required
def unfollow(request):
    try:
        user_id = request.GET['user-id']
        to_user = get_object_or_404(User, pk=user_id)
        from_user = request.user

        following = from_user.profile.get_following()

        if to_user in following:
            activity = Activity.objects.get(from_user=from_user, to_user=to_user, activity_type=Activity.FOLLOW)
            activity.delete()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
    except:
        return HttpResponseBadRequest()


def update_followers_count(request):
    try:
        user_id = request.GET['user-id']
        user = get_object_or_404(User, pk=user_id)
        followers_count = user.profile.get_followers_count()
        return HttpResponse(followers_count)
    except:
        return HttpResponseBadRequest()

def following(request, username):
    page_user = get_object_or_404(User, username=username)
    page_title = 'following'
    following = page_user.profile.get_following()
    user_following = None

    if request.user.is_authenticated():
        user_following = request.user.profile.get_following()

    return render(request, 'activities/follow.html', {
            'page_user': page_user,
            'page_title': page_title,
            'follow_list': following,
            'user_following': user_following
        })

def followers(request, username):
    user = get_object_or_404(User, username=username)
    page_title = 'followers'
    followers = user.profile.get_followers()
    user_following = None

    if request.user.is_authenticated():
        user_following = request.user.profile.get_following()

    return render(request, 'activities/follow.html', {
            'page_user': user,
            'page_title': page_title,
            'follow_list': followers,
            'user_following': user_following
         })

