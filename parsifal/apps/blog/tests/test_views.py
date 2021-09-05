from django.test import TestCase
from django.urls import reverse

from parsifal.apps.authentication.tests.factories import SuperUserFactory
from parsifal.apps.blog.models import Entry
from parsifal.apps.blog.tests.factories import EntryFactory


class TestBlogViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = SuperUserFactory()
        cls.entry_1 = EntryFactory(title="Test Entry #1", status=Entry.PUBLISHED, created_by=user)
        cls.entry_2 = EntryFactory(title="Test Entry #2", status=Entry.PUBLISHED, created_by=user)
        cls.entry_3 = EntryFactory(title="Test Entry #3", status=Entry.DRAFT, created_by=user)

    def test_entries_view(self):
        url = reverse("blog:entries")
        response = self.client.get(url)

        with self.subTest(msg="Test status code"):
            self.assertEqual(200, response.status_code)

        parts = (self.entry_1.title, self.entry_2.title)
        for part in parts:
            with self.subTest(msg="Test response body", part=part):
                self.assertContains(response, part)

        with self.subTest(msg="Test not published entry"):
            self.assertNotContains(response, self.entry_3.title)

    def test_entry_view_success(self):
        url = reverse("blog:entry", args=(self.entry_1.slug,))
        response = self.client.get(url)

        with self.subTest(msg="Test status code"):
            self.assertEqual(200, response.status_code)

        with self.subTest(msg="Test response body"):
            self.assertContains(response, self.entry_1.title)

    def test_entry_view_not_found(self):
        url = reverse("blog:entry", args=(self.entry_3.slug,))
        response = self.client.get(url)

        with self.subTest(msg="Test status code"):
            self.assertEqual(404, response.status_code)
