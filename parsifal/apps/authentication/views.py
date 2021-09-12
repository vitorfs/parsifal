from django.contrib import messages
from django.contrib.auth import login
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView

from parsifal.apps.authentication.forms import SignUpForm
from parsifal.apps.invites.constants import InviteStatus
from parsifal.apps.invites.models import Invite


@method_decorator([sensitive_post_parameters(), csrf_protect, never_cache], name="dispatch")
class SignUpView(FormView):
    form_class = SignUpForm
    template_name = "registration/signup.html"

    @cached_property
    def invite(self):
        try:
            code = self.request.GET.get("invite", self.request.POST.get("invite"))
            return Invite.objects.filter(invitee=None, status=InviteStatus.PENDING).get(code=code)
        except (Invite.DoesNotExist, ValidationError):
            return None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(request=self.request, initial={"invite": self.invite})
        return kwargs

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, _("Your account was successfully created."))
        return redirect(user)

    def form_invalid(self, form):
        messages.error(
            self.request,
            _(
                "There were some problems while creating your account. "
                "Please review the form below before submitting it again."
            ),
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        kwargs.update(invite=self.invite)
        return super().get_context_data(**kwargs)
