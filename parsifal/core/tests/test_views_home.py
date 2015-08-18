# coding: utf-8

from django.test import TestCase, Client

class HomeUnsignedUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/')

    def test_get(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/cover.html')
