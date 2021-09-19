from django.contrib.auth.models import User
from django.test.testcases import TestCase
from django.urls import reverse

from parsifal.apps.authentication.tests.factories import UserFactory
from parsifal.apps.reviews.models import Review, Source
from parsifal.apps.reviews.tests.factories import DefaultSourceFactory, ReviewFactory, SourceFactory


class TestDeleteReviewView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = UserFactory()
        cls.co_author = UserFactory()
        cls.default_source = DefaultSourceFactory()
        cls.review_source = SourceFactory()
        cls.review = ReviewFactory(
            author=cls.author, co_authors=[cls.co_author], sources=[cls.default_source, cls.review_source]
        )
        cls.url = reverse("delete_review", args=(cls.review.author.username, cls.review.name))

    def test_setup(self):
        self.assertEqual(2, User.objects.count())
        self.assertEqual(2, Source.objects.count())
        self.assertEqual(self.co_author, self.review.co_authors.first())

    def test_get_not_allowed(self):
        self.client.force_login(self.author)
        response = self.client.get(self.url)
        self.assertEqual(405, response.status_code)

    def test_login_required(self):
        response = self.client.post(self.url)
        with self.subTest(msg="Test status code"):
            self.assertEqual(404, response.status_code)
        with self.subTest(msg="Test review not deleted"):
            self.assertTrue(Review.objects.filter(pk=self.review.pk).exists())
            self.assertEqual(2, Source.objects.count())

    def test_main_author_required(self):
        self.client.force_login(self.co_author)
        response = self.client.post(self.url)
        with self.subTest(msg="Test status code"):
            self.assertEqual(403, response.status_code)
        with self.subTest(msg="Test review not deleted"):
            self.assertTrue(Review.objects.filter(pk=self.review.pk).exists())
            self.assertEqual(2, Source.objects.count())

    def test_delete_successful(self):
        self.client.force_login(self.author)
        response = self.client.post(self.url, follow=True)

        with self.subTest(msg="Test post status code"):
            self.assertEqual(302, response.redirect_chain[0][1])

        with self.subTest(msg="Test post redirect status code"):
            self.assertEqual(200, response.status_code)

        with self.subTest(msg="Test review deleted"):
            self.assertFalse(Review.objects.filter(pk=self.review.pk).exists())
            self.assertEqual(1, Source.objects.count())

        with self.subTest(msg="Test default source not deleted"):
            self.assertTrue(Source.objects.filter(pk=self.default_source.pk).exists())
