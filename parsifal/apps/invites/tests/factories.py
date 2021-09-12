import factory
from factory.django import DjangoModelFactory

from parsifal.apps.invites.models import Invite
from parsifal.apps.reviews.tests.factories import ReviewFactory


class InviteFactory(DjangoModelFactory):
    review = factory.SubFactory(ReviewFactory)
    invited_by = factory.SelfAttribute("review.author")
    invitee_email = factory.Sequence(lambda n: f"invitee-{n}@example.com")

    class Meta:
        model = Invite
