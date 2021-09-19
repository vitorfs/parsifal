from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext, gettext_lazy as _
from django.views import View
from django.views.generic import UpdateView

from parsifal.apps.reviews.decorators import main_author_required
from parsifal.apps.reviews.mixins import MainAuthorRequiredMixin, ReviewMixin
from parsifal.apps.reviews.models import Review
from parsifal.apps.reviews.settings.forms import ReviewSettingsForm


class UpdateReviewSettingsView(MainAuthorRequiredMixin, ReviewMixin, SuccessMessageMixin, UpdateView):
    model = Review
    form_class = ReviewSettingsForm
    template_name = "settings/review_settings.html"
    success_message = _("Review updated with success!")

    def get_object(self, queryset=None):
        return self.review

    def get_success_url(self):
        return reverse("settings", args=(self.review.author.username, self.review.name))


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


class DeleteReviewView(MainAuthorRequiredMixin, ReviewMixin, View):
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
