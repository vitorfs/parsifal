from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from parsifal.apps.invites.forms import SendInviteForm
from parsifal.apps.invites.models import Invite
from parsifal.apps.reviews.mixins import AuthorRequiredMixin, ReviewMixin


class ManageAccessView(LoginRequiredMixin, AuthorRequiredMixin, ReviewMixin, CreateView):
    model = Invite
    form_class = SendInviteForm
    template_name = "invites/manage_access.html"

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
