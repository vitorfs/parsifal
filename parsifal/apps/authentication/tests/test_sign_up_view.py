from django.contrib.auth.models import User
from django.test.testcases import TestCase
from django.urls import reverse


class TestSignUpView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("signup")

    def test_get_success(self):
        response = self.client.get(self.url)
        with self.subTest(msg="Test get status code"):
            self.assertEqual(200, response.status_code)

        parts = ("csrfmiddlewaretoken", "username", "email", "password1", "password2")
        for part in parts:
            with self.subTest(msg="Test response body", part=part):
                self.assertContains(response, part)

    def test_post_success(self):
        data = {
            "username": "jane",
            "email": "jane.doe@example.com",
            "password1": "S3cr3tPass",
            "password2": "S3cr3tPass",
        }
        response = self.client.post(self.url, data, follow=True)

        with self.subTest(msg="Test post status code"):
            self.assertEqual(302, response.redirect_chain[0][1])

        with self.subTest(msg="Test post redirect status code"):
            self.assertEqual(200, response.status_code)

        with self.subTest(msg="Test user authenticated after sign up"):
            self.assertTrue(response.context["user"].is_authenticated)

        with self.subTest(msg="Test success message"):
            self.assertContains(response, "Your account was successfully created.")

        with self.subTest(msg="Test user created"):
            self.assertTrue(User.objects.filter(username="jane").exists())

    def test_post_fail(self):
        data = {
            "username": "jane",
            "email": "jane.doe@example.com",
            "password1": "123",
            "password2": "321",
        }
        response = self.client.post(self.url, data)

        with self.subTest(msg="Test post status code"):
            self.assertEqual(200, response.status_code)

        with self.subTest(msg="Test error message"):
            self.assertContains(response, "There were some problems while creating your account.")

        with self.subTest(msg="Test user not created"):
            self.assertFalse(User.objects.filter(username="jane").exists())
