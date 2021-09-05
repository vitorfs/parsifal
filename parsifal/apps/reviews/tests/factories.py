import factory
from factory.django import DjangoModelFactory

from parsifal.apps.authentication.tests.factories import UserFactory
from parsifal.apps.reviews.models import Review


class ReviewFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"slr-{n}")
    title = factory.Sequence(lambda n: f"Test SLR #{n}")
    author = factory.SubFactory(UserFactory)

    class Meta:
        model = Review
        django_get_or_create = ("name",)
