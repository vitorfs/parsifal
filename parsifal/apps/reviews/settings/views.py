from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse as r
from django.utils.text import slugify
from django.utils.translation import gettext
from django.views import View

from parsifal.apps.reviews.decorators import main_author_required
from parsifal.apps.reviews.mixins import MainAuthorRequiredMixin, ReviewMixin
from parsifal.apps.reviews.models import Review
from parsifal.apps.reviews.settings.forms import ReviewSettingsForm


@main_author_required
@login_required
def settings(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username__iexact=username)
    if request.method == "POST":
        form = ReviewSettingsForm(request.POST, instance=review)
        if form.is_valid():
            name = slugify(form.instance.name)
            unique_name = name
            if unique_name != review_name:
                i = 0
                while Review.objects.filter(name=unique_name, author__username=review.author.username):
                    i = i + 1
                    unique_name = "{0}-{1}".format(name, i)
            form.instance.name = unique_name
            review = form.save()
            messages.success(request, "Review was saved successfully.")
            return redirect(r("settings", args=(review.author.username, unique_name)))
    else:
        form = ReviewSettingsForm(instance=review)
    return render(request, "settings/review_settings.html", {"review": review, "form": form})


@main_author_required
@login_required
def transfer(request):
    try:
        review_id = request.POST["review-id"]
        transfer_user_username = request.POST["transfer-user"]
        review = Review.objects.get(pk=review_id)
        try:
            transfer_user = User.objects.get(username=transfer_user_username)
        except Exception:
            messages.warning(request, "User not found.")
            return redirect("settings", review.author.username, review.name)

        current_user = request.user
        if current_user != transfer_user:
            if transfer_user in review.co_authors.all():
                review.co_authors.remove(transfer_user)
            review.author = transfer_user
            review.co_authors.add(current_user)
            review.save()
            return redirect("review", review.author.username, review.name)
        else:
            messages.warning(request, "Hey! You can't transfer the review to yourself.")
            return redirect("settings", review.author.username, review.name)

    except Exception:
        return HttpResponseBadRequest("Something went wrong.")


class DeleteReviewView(LoginRequiredMixin, MainAuthorRequiredMixin, ReviewMixin, View):
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        sources = self.review.sources.all()
        for source in sources:
            if not source.is_default:
                self.review.sources.remove(source)
                source.delete()
        self.review.delete()
        messages.success(request, gettext("The review was deleted with success."))
        return redirect(request.user)
