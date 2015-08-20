# coding: utf-8

from django.test import TestCase
from django.contrib.auth.models import User

from parsifal.reviews.models import Review, Source


class ImportBibitexTest(TestCase):
    fixtures = ['source_initial_data.json',]

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='john', email='john.doe@parsif.al', password='123')
        cls.review = Review.objects.create(name='test-review', title='Test Review', description='', author=cls.user, objective='')

    def setUp(self):
        self.client.login(username='john', password='123')

    def test_loaded_fixture(self):
        self.assertGreater(User.objects.all().count(), 0)
        self.assertGreater(Source.objects.all().count(), 0)
        self.assertGreater(Review.objects.all().count(), 0)
