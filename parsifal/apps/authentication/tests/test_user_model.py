from django.test.testcases import TestCase
from django.urls import reverse

from parsifal.apps.authentication.tests.factories import UserFactory


class TestUserModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(username="john.doe")

    def test_get_absolute_url(self):
        expected_url = reverse("reviews", args=(self.user.username,))
        self.assertEqual(self.user.get_absolute_url(), expected_url)
        self.assertEqual(expected_url, "/john.doe/")
