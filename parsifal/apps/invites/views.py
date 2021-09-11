from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DetailView

from parsifal.apps.invites.forms import SendInviteForm
from parsifal.apps.invites.models import Invite
from parsifal.apps.reviews.mixins import AuthorRequiredMixin, ReviewMixin
from parsifal.utils.mask import mask_email


class ManageAccessView(LoginRequiredMixin, AuthorRequiredMixin, ReviewMixin, CreateView):
    model = Invite
    form_class = SendInviteForm
    template_name = "invites/manage_access.html"

    def get_success_url(self):
        return reverse("invites:manage_access", args=(self.review.author.username, self.review.name))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(request=self.request, review=self.review)
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs.update(
            {
                "invites": self.review.invites.select_related("invited_by__profile", "invitee__profile").order_by(
                    "-date_sent"
                )
            }
        )
        return super().get_context_data(**kwargs)


class InviteDetail(ReviewMixin, DetailView):
    model = Invite
    pk_url_kwarg = "invite_id"
    slug_url_kwarg = "code"
    slug_field = "code"
    query_pk_and_slug = True
    context_object_name = "invite"

    def get_queryset(self):
        return self.review.invites.all()

    def get_context_data(self, **kwargs):
        kwargs.update(invitee_masked_email=mask_email(self.object.get_invitee_email()))
        return super().get_context_data(**kwargs)
