from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property

from parsifal.apps.reviews.models import Review


class ReviewMixin:
    """
    This mixin is usually used together with a view that inherits from
    ContextMixin.
    """

    @cached_property
    def review(self):
        queryset = Review.objects.select_related("author__profile").prefetch_related("co_authors__profile")
        return get_object_or_404(
            queryset, name=self.kwargs.get("review_name"), author__username=self.kwargs.get("username")
        )

    def get_context_data(self, **kwargs):
        kwargs.update(review=self.review)
        return super().get_context_data(**kwargs)


class MainAuthorRequiredMixin(UserPassesTestMixin):
    """
    This mixin depends on having a review property on the view class.
    It is usually used together with the ReviewMixin
    """

    def test_func(self):
        return self.review.author == self.request.user


class AuthorRequiredMixin(UserPassesTestMixin):
    """
    This mixin depends on having a review property on the view class.
    It is usually used together with the ReviewMixin
    """

    def test_func(self):
        return self.review.is_author_or_coauthor(self.request.user)
