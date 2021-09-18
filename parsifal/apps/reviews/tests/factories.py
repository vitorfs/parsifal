import factory
from factory.django import DjangoModelFactory

from parsifal.apps.authentication.tests.factories import UserFactory
from parsifal.apps.reviews.models import Review, Source


class ReviewFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"slr-{n}")
    title = factory.Sequence(lambda n: f"Test SLR #{n}")
    author = factory.SubFactory(UserFactory)

    class Meta:
        model = Review
        django_get_or_create = ("name",)

    @factory.post_generation
    def co_authors(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.co_authors.add(*extracted)

    @factory.post_generation
    def sources(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.sources.add(*extracted)


class SourceFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Source #{n}")
    url = factory.Sequence(lambda n: f"https://source-{n}.example.com")
    is_default = False

    class Meta:
        model = Source
        django_get_or_create = ("name",)


class DefaultSourceFactory(SourceFactory):
    is_default = True
