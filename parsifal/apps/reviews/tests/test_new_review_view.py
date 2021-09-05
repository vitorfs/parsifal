from django.test.testcases import TestCase
from django.urls import reverse

from parsifal.apps.authentication.tests.factories import UserFactory
from parsifal.apps.reviews.tests.factories import ReviewFactory
from parsifal.utils.test import login_redirect_url


class TestNewReviewView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.url = reverse("reviews:new")

    def test_login_required(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, login_redirect_url(self.url))

    def test_get_success(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        with self.subTest(msg="Test get status code"):
            self.assertEqual(200, response.status_code)

        parts = ("csrfmiddlewaretoken", "title", "description")
        for part in parts:
            with self.subTest(msg="Test response body", part=part):
                self.assertContains(response, part)

    def test_post_success(self):
        data = {"title": "Test SLR", "description": "This is a test SLR"}
        self.client.force_login(self.user)
        response = self.client.post(self.url, data, follow=True)
        with self.subTest(msg="Test post status code"):
            self.assertEqual(302, response.redirect_chain[0][1])

        with self.subTest(msg="Test post redirect status code"):
            self.assertEqual(200, response.status_code)

        with self.subTest(msg="Test success message"):
            self.assertContains(response, "Review created successfully.")

        review = self.user.review_set.first()

        with self.subTest(msg="Test generated slug"):
            self.assertEqual("test-slr", review.name)

    def test_post_fail(self):
        data = {"title": "", "description": ""}
        self.client.force_login(self.user)
        response = self.client.post(self.url, data, follow=True)

        with self.subTest(msg="Test post status code"):
            self.assertEqual(200, response.status_code)

        with self.subTest(msg="Test error message"):
            self.assertContains(response, "This field is required.")

        with self.subTest(msg="No review created"):
            self.assertFalse(self.user.review_set.exists())

    def test_post_conflicting_slug(self):
        ReviewFactory(author=self.user, name="test-slr")
        data = {"title": "Test SLR", "description": "This is a test SLR"}
        self.client.force_login(self.user)
        response = self.client.post(self.url, data, follow=True)

        with self.subTest(msg="Test post redirect status code"):
            self.assertEqual(200, response.status_code)

        with self.subTest(msg="Test review created"):
            self.assertEqual(2, self.user.review_set.count())

        review = self.user.review_set.order_by("-id").first()

        with self.subTest(msg="Test generated slug"):
            self.assertEqual("test-slr-1", review.name)

    def test_post_invalid_slug(self):
        data = {"title": ")", "description": "This is a test SLR"}
        self.client.force_login(self.user)
        response = self.client.post(self.url, data, follow=True)

        with self.subTest(msg="Test post redirect status code"):
            self.assertEqual(200, response.status_code)

        review = self.user.review_set.first()

        with self.subTest(msg="Test review created"):
            self.assertIsNotNone(review)

        with self.subTest(msg="Test generated slug"):
            self.assertEqual("literature-review", review.name)
