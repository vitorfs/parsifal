from django.test.testcases import TestCase
from django.urls import reverse

from parsifal.apps.authentication.tests.factories import UserFactory
from parsifal.utils.test import login_redirect_url


class TestUpdateProfileView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(first_name="VITOR")
        cls.url = reverse("settings:profile")

    def test_login_required(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, login_redirect_url(self.url))

    def test_get_success(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        with self.subTest(msg="Test get status code"):
            self.assertEqual(200, response.status_code)

        parts = ("csrfmiddlewaretoken", "first_name", "last_name", "public_email", "VITOR")
        for part in parts:
            with self.subTest(msg="Test response body", part=part):
                self.assertContains(response, part)

    def test_post_success(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "public_email": "john.doe@example.com",
            "url": "https://example.com",
            "institution": "University of Oulu",
            "location": "Oulu",
        }
        self.client.force_login(self.user)
        response = self.client.post(self.url, data, follow=True)
        with self.subTest(msg="Test post status code"):
            self.assertEqual(302, response.redirect_chain[0][1])

        with self.subTest(msg="Test post redirect status code"):
            self.assertEqual(200, response.status_code)

        with self.subTest(msg="Test success message"):
            self.assertContains(response, "Your profile was updated with success!")

        for value in data.values():
            with self.subTest(msg="Test form saved data", value=value):
                self.assertContains(response, f'value="{value}"')

    def test_post_fail(self):
        data = {"url": "x" * 100}  # invalid url with 100 chars
        self.client.force_login(self.user)
        response = self.client.post(self.url, data)

        with self.subTest(msg="Test post status code"):
            self.assertEqual(200, response.status_code)

        with self.subTest(msg="Test error message"):
            self.assertContains(response, "Ensure this value has at most 50 characters (it has 100).")
