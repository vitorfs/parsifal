from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, UpdateView

from parsifal.apps.invites.constants import InviteStatus
from parsifal.apps.reviews.decorators import author_required, main_author_required
from parsifal.apps.reviews.forms import CreateReviewForm, UpdateReviewForm
from parsifal.apps.reviews.mixins import AuthorRequiredMixin, ReviewMixin
from parsifal.apps.reviews.models import Review


def reviews(request, username):
    user = get_object_or_404(User, username__iexact=username)
    followers = user.profile.get_followers()
    is_following = False
    if request.user in followers:
        is_following = True

    followers_count = user.profile.get_followers_count()
    following_count = user.profile.get_following_count()

    user_reviews = user.profile.get_reviews()

    pending_invites = user.invites_received.filter(status=InviteStatus.PENDING)
    pending_invites_count = pending_invites.count()

    return render(
        request,
        "reviews/reviews.html",
        {
            "user_reviews": user_reviews,
            "page_user": user,
            "is_following": is_following,
            "following_count": following_count,
            "followers_count": followers_count,
            "pending_invites": pending_invites,
            "pending_invites_count": pending_invites_count,
        },
    )


class CreateReviewView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Review
    form_class = CreateReviewForm
    success_message = _("Review created with success!")
    template_name = "reviews/new.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(request=self.request)
        return kwargs


class UpdateReviewView(AuthorRequiredMixin, ReviewMixin, SuccessMessageMixin, UpdateView):
    model = Review
    form_class = UpdateReviewForm
    success_message = _("Review updated with success!")
    template_name = "reviews/review.html"

    def get_object(self, queryset=None):
        return self.review


@main_author_required
@login_required
@require_POST
def remove_author_from_review(request):
    try:
        author_id = request.POST.get("user-id")
        review_id = request.POST.get("review-id")
        author = User.objects.get(pk=author_id)
        review = Review.objects.get(pk=review_id)
        review.co_authors.remove(author)
        review.save()
        return HttpResponse()
    except Exception:
        return HttpResponseBadRequest()


@author_required
@login_required
def save_description(request):
    try:
        review_id = request.POST["review-id"]
        description = request.POST["description"]
        review = Review.objects.get(pk=review_id)
        if len(description) > 500:
            return HttpResponseBadRequest(
                "The review description should not exceed 500 characters. The given description have %s characters."
                % len(description)
            )
        else:
            review.description = description
            review.save()
            return HttpResponse("Your review has been saved successfully!")
    except Exception:
        return HttpResponseBadRequest()


@author_required
@login_required
def leave(request):
    review_id = request.POST.get("review-id")
    review = get_object_or_404(Review, pk=review_id)
    review.co_authors.remove(request.user)
    review.save()
    messages.add_message(request, messages.SUCCESS, "You successfully left the review {0}.".format(review.title))
    return redirect("/" + request.user.username + "/")
