from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from activities.models import Activity
from django.contrib.auth.models import User
from parsifal.decorators import ajax_required

@ajax_required
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

@ajax_required
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

def following(request, username):
    user = get_object_or_404(User, username=username)
    page_title = 'following'
    following = user.profile.get_following()
    context = RequestContext(request, {'page_user': user, 'page_title': page_title, 'follow_list': following})
    return render_to_response('activities/follow.html', context)

def followers(request, username):
    user = get_object_or_404(User, username=username)
    page_title = 'followers'
    followers = user.profile.get_followers()
    context = RequestContext(request, {'page_user': user, 'page_title': page_title, 'follow_list': followers })
    return render_to_response('activities/follow.html', context)