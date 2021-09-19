from django.test.testcases import TestCase
from django.urls import reverse

from parsifal.apps.reviews.tests.factories import ReviewFactory


class TestReviewModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.review = ReviewFactory(author__username="john.doe", name="literature-review")

    def test_get_absolute_url(self):
        """
        Some views rely on the get_absolute_url to redirect the user to the
        correct application flow. If you are changing the review URL make sure
        to review all related views.
        """
        expected_url = reverse("review", args=("john.doe", "literature-review"))
        self.assertEqual(self.review.get_absolute_url(), expected_url)
        self.assertEqual(expected_url, "/john.doe/literature-review/")
