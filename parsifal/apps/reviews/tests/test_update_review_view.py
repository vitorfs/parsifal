from django.test.testcases import TestCase
from django.urls import reverse

from parsifal.apps.authentication.tests.factories import UserFactory
from parsifal.apps.reviews.tests.factories import ReviewFactory


class TestUpdateReviewView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.co_author = UserFactory()
        cls.non_author = UserFactory()
        cls.review = ReviewFactory(
            title="Initial Title", description="Initial Description", author=cls.user, co_authors=[cls.co_author]
        )
        cls.url = reverse("review", args=(cls.user.username, cls.review.name))

    def test_login_required(self):
        """
        For review pages we always return 404 for non authorized access so
        to not differentiate between existing and non existing reviews
        """
        response = self.client.get(self.url)
        self.assertEqual(404, response.status_code)

    def test_get_success_main_author(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        with self.subTest(msg="Test get status code"):
            self.assertEqual(200, response.status_code)

        parts = ("csrfmiddlewaretoken", "title", "description")
        for part in parts:
            with self.subTest(msg="Test response body", part=part):
                self.assertContains(response, part)

    def test_get_success_co_author(self):
        self.client.force_login(self.co_author)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_get_fail_non_author(self):
        """
        For review pages we always return 404 for non authorized access so
        to not differentiate between existing and non existing reviews
        """
        self.client.force_login(self.non_author)
        response = self.client.get(self.url)
        self.assertEqual(404, response.status_code)

    def test_post_success(self):
        data = {"title": "Test SLR", "description": "This is a test SLR"}
        self.client.force_login(self.user)
        response = self.client.post(self.url, data, follow=True)
        with self.subTest(msg="Test post status code"):
            self.assertEqual(302, response.redirect_chain[0][1])

        with self.subTest(msg="Test post redirect status code"):
            self.assertEqual(200, response.status_code)

        with self.subTest(msg="Test success message"):
            self.assertContains(response, "Review updated with success!")

        self.review.refresh_from_db()

        with self.subTest(msg="Test data changed"):
            self.assertEqual("Test SLR", self.review.title)
            self.assertEqual("This is a test SLR", self.review.description)

    def test_post_fail(self):
        data = {"title": "", "description": ""}
        self.client.force_login(self.user)
        response = self.client.post(self.url, data, follow=True)

        with self.subTest(msg="Test post status code"):
            self.assertEqual(200, response.status_code)

        with self.subTest(msg="Test error message"):
            self.assertContains(response, "This field is required.")

        self.review.refresh_from_db()

        with self.subTest(msg="Test data did not change"):
            self.assertEqual("Initial Title", self.review.title)
            self.assertEqual("Initial Description", self.review.description)
