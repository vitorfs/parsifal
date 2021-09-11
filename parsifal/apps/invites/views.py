from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, DetailView

from parsifal.apps.invites.constants import InviteStatus
from parsifal.apps.invites.forms import SendInviteForm
from parsifal.apps.invites.models import Invite
from parsifal.apps.reviews.mixins import MainAuthorRequiredMixin, ReviewMixin
from parsifal.utils.mask import mask_email


class ManageAccessView(LoginRequiredMixin, MainAuthorRequiredMixin, ReviewMixin, SuccessMessageMixin, CreateView):
    model = Invite
    form_class = SendInviteForm
    template_name = "invites/manage_access.html"

    def get_success_url(self):
        return reverse("invites:manage_access", args=(self.review.author.username, self.review.name))

    def get_success_message(self, cleaned_data):
        return _("An invitation was sent to %s.") % self.object.get_invitee_email()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(request=self.request, review=self.review)
        return kwargs

    def get_context_data(self, **kwargs):
        invites = self.review.invites.select_related("invited_by__profile", "invitee__profile").order_by("-date_sent")
        kwargs.update(invites=invites)
        return super().get_context_data(**kwargs)


class InviteDeleteView(LoginRequiredMixin, MainAuthorRequiredMixin, ReviewMixin, DeleteView):
    model = Invite
    pk_url_kwarg = "invite_id"
    context_object_name = "invite"

    def get_queryset(self):
        return self.review.invites.all()

    def get_success_url(self):
        return reverse("invites:manage_access", args=(self.review.author.username, self.review.name))

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, _("The invitation was removed with success."))
        return response


class InviteDetailView(DetailView):
    model = Invite
    slug_field = "code"
    slug_url_kwarg = "code"
    context_object_name = "invite"

    def get_queryset(self):
        return Invite.objects.filter(status=InviteStatus.PENDING)

    def get_context_data(self, **kwargs):
        kwargs.update(invitee_masked_email=mask_email(self.object.get_invitee_email()))
        return super().get_context_data(**kwargs)
