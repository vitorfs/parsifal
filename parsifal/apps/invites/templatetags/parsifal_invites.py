from django import template
from django.utils.html import format_html

from parsifal.apps.invites.constants import InviteStatus

register = template.Library()


@register.simple_tag()
def invite_status(invite):
    css_classes = {
        InviteStatus.PENDING: "label-warning",
        InviteStatus.ACCEPTED: "label-success",
        InviteStatus.REJECTED: "label-danger",
    }
    return format_html(
        "<span class='label {css_class}'>{label}</span>",
        css_class=css_classes.get(invite.status),
        label=invite.get_status_display(),
    )
