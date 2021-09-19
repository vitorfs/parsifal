from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
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
            queryset, name=self.kwargs.get("review_name"), author__username__iexact=self.kwargs.get("username")
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
        return self.request.user.is_authenticated and self.review.author == self.request.user

    def handle_no_permission(self):
        """
        return a 404 status code to not leak metadata indicating that a given
        review exists or not
        """
        if self.review.co_authors.filter(pk=self.request.user.pk).exists():
            # if the user is a co-author, they already know that this particular
            # review exists, so raise a more adequate exception
            super().handle_no_permission()
        else:
            # if not, just return 404 to not leak any further information
            raise Http404


class AuthorRequiredMixin(UserPassesTestMixin):
    """
    This mixin depends on having a review property on the view class.
    It is usually used together with the ReviewMixin
    """

    def test_func(self):
        return self.request.user.is_authenticated and (
            self.review.author == self.request.user or self.review.co_authors.filter(pk=self.request.user.pk).exists()
        )

    def handle_no_permission(self):
        """
        return a 404 status code to not leak metadata indicating that a given
        review exists or not
        """
        raise Http404
