from django.contrib.auth.models import User
from django.test.testcases import TestCase

from parsifal.apps.authentication.forms import SignUpForm
from parsifal.apps.authentication.tests.factories import UserFactory


class TestSignUpForm(TestCase):
    def test_form_success(self):
        data = {
            "username": "jane",
            "email": "JANE.DOE@EXAMPLE.COM",
            "password1": "O99(d3!cx",
            "password2": "O99(d3!cx",
        }
        form = SignUpForm(data=data)

        with self.subTest(msg="Test form is valid"):
            self.assertTrue(form.is_valid())

        user = form.save()
        with self.subTest(msg="Test user created"):
            self.assertIsNotNone(user)

        with self.subTest(msg="Test user saved on database"):
            self.assertTrue(User.objects.filter(username="jane").exists())

        with self.subTest(msg="Test email normalized"):
            self.assertEqual("JANE.DOE@example.com", user.email)

    def test_form_invalid(self):
        data = {
            "username": "joão",
            "email": "joao@example.com",
            "password1": "O99(d3!cx",
            "password2": "O99(d3!cx",
        }
        form = SignUpForm(data=data)

        with self.subTest(msg="Test form is valid"):
            self.assertFalse(form.is_valid())

        with self.subTest(msg="Test form errors"):
            msg = "Enter a valid username. This value may contain only English letters, numbers, and . _ characters."
            self.assertEqual(msg, form.errors["username"][0])

    def test_form_invalid_username_and_email_case_insensitive(self):
        UserFactory(username="john", email="john.doe@example.com")

        data = {
            "username": "JOHN",
            "email": "JOHN.DOE@EXAMPLE.COM",
            "password1": "O99(d3!cx",
            "password2": "O99(d3!cx",
        }
        form = SignUpForm(data=data)

        with self.subTest(msg="Test form is valid"):
            self.assertFalse(form.is_valid())

        with self.subTest(msg="Test username form error"):
            self.assertEqual("A user with that username already exists.", form.errors["username"][0])

        with self.subTest(msg="Test username form error"):
            self.assertEqual("A user with that email already exists.", form.errors["email"][0])
