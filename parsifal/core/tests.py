# coding: utf-8

from django.test import TestCase


class HomepageTest(TestCase):
    def test_get(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'core/cover.html')
