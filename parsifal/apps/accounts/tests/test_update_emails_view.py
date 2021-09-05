from django.test.testcases import TestCase
from django.urls import reverse

from parsifal.apps.authentication.tests.factories import UserFactory
from parsifal.utils.test import login_redirect_url


class TestUpdateEmailsViewView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(email="john.doe@example.com")
        cls.url = reverse("settings:emails")

    def test_login_required(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, login_redirect_url(self.url))

    def test_get_success(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        with self.subTest(msg="Test get status code"):
            self.assertEqual(200, response.status_code)

        parts = ("csrfmiddlewaretoken", "email", "john.doe@example.com")
        for part in parts:
            with self.subTest(msg="Test response body", part=part):
                self.assertContains(response, part)

    def test_post_success(self):
        data = {
            "email": "doe.john@example.com",
        }
        self.client.force_login(self.user)
        response = self.client.post(self.url, data, follow=True)
        with self.subTest(msg="Test post status code"):
            self.assertEqual(302, response.redirect_chain[0][1])

        with self.subTest(msg="Test post redirect status code"):
            self.assertEqual(200, response.status_code)

        with self.subTest(msg="Test success message"):
            self.assertContains(response, "Account email was updated with success!")

        with self.subTest(msg="Test form saved data"):
            self.assertContains(response, 'value="doe.john@example.com"')

    def test_post_fail(self):
        data = {"email": "invalidemail"}
        self.client.force_login(self.user)
        response = self.client.post(self.url, data)

        with self.subTest(msg="Test post status code"):
            self.assertEqual(200, response.status_code)

        with self.subTest(msg="Test error message"):
            self.assertContains(response, "Enter a valid email address.")
