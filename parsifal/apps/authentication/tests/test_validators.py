from django.core.exceptions import ValidationError
from django.test.testcases import TestCase

from parsifal.apps.authentication.tests.factories import UserFactory
from parsifal.apps.authentication.validators import (
    validate_case_insensitive_email,
    validate_case_insensitive_username,
    validate_forbidden_usernames,
)


class TestValidateForbiddenUsernames(TestCase):
    def test_valid(self):
        validate_forbidden_usernames("john.doe")

    def test_invalid(self):
        with self.assertRaisesMessage(ValidationError, "This is a reserved word."):
            validate_forbidden_usernames("admin")

    def test_invalid_uppercase(self):
        with self.assertRaisesMessage(ValidationError, "This is a reserved word."):
            validate_forbidden_usernames("ADMIN")


class TestValidateCaseInsensitiveEmail(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(email="john.doe@example.com")

    def test_valid(self):
        validate_case_insensitive_email("jane.doe@example.com")

    def test_invalid(self):
        with self.assertRaisesMessage(ValidationError, "A user with that email already exists."):
            validate_case_insensitive_email("john.doe@example.com")

    def test_invalid_uppercase(self):
        with self.assertRaisesMessage(ValidationError, "A user with that email already exists."):
            validate_case_insensitive_email("JOHN.DOE@example.com")


class TestValidateCaseInsensitiveUsername(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(username="john.doe")

    def test_valid(self):
        validate_case_insensitive_username("jane.doe")

    def test_invalid(self):
        with self.assertRaisesMessage(ValidationError, "A user with that username already exists."):
            validate_case_insensitive_username("john.doe")

    def test_invalid_uppercase(self):
        with self.assertRaisesMessage(ValidationError, "A user with that username already exists."):
            validate_case_insensitive_username("JOHN.DOE")
