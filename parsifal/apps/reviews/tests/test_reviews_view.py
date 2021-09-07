from django.test.testcases import TestCase
from django.urls import reverse

from parsifal.apps.authentication.tests.factories import UserFactory
from parsifal.apps.reviews.tests.factories import ReviewFactory


class TestReviewsView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.review = ReviewFactory(title="TEST_REVIEW")
        cls.url = reverse("reviews", args=(cls.review.author.username,))

    def test_get_success(self):
        response = self.client.get(self.url)
        with self.subTest(msg="Test get status code"):
            self.assertEqual(200, response.status_code)

        with self.subTest(msg="Test unpublished review not visible"):
            self.assertNotContains(response, self.review.title)

    def test_get_success_authenticated(self):
        self.client.force_login(self.review.author)
        response = self.client.get(self.url)
        with self.subTest(msg="Test get status code"):
            self.assertEqual(200, response.status_code)

        with self.subTest(msg="Test unpublished review visible to author"):
            self.assertContains(response, self.review.title)

    def test_get_success_authenticated_other_user(self):
        """
        Test if only the authenticated author can see the unpublished review
        """
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.get(self.url)
        with self.subTest(msg="Test get status code"):
            self.assertEqual(200, response.status_code)

        with self.subTest(msg="Test unpublished review only visible to author"):
            self.assertNotContains(response, self.review.title)
