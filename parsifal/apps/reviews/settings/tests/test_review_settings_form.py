from django.test.testcases import TestCase

from parsifal.apps.authentication.tests.factories import UserFactory
from parsifal.apps.reviews.settings.forms import ReviewSettingsForm
from parsifal.apps.reviews.tests.factories import ReviewFactory


class TestReviewSettingsForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.other_user = UserFactory()
        cls.author = UserFactory()
        cls.review = ReviewFactory(name="abc", author=cls.author)
        cls.review_2 = ReviewFactory(name="abc-2", author=cls.author)

    def test_setup(self):
        self.assertNotEqual(self.other_user, self.review.author)

    def test_disabled_field_ignored(self):
        data = {"name": "efg", "author": self.other_user.pk}
        form = ReviewSettingsForm(data=data, instance=self.review)

        with self.subTest(msg="Test if form is valid"):
            self.assertTrue(form.is_valid())

        form.save()

        self.review.refresh_from_db()

        with self.subTest(msg="Test author did not change"):
            self.assertNotEqual(self.review.author, self.other_user)

        with self.subTest(msg="Test review name changed"):
            self.assertEqual("efg", self.review.name)

    def test_unique_together_validation(self):
        """
        Try to set the same review name as an existing review of the same user
        """
        data = {"name": "abc", "author": self.author.pk}
        form = ReviewSettingsForm(data=data, instance=self.review_2)
        self.assertFalse(form.is_valid())
