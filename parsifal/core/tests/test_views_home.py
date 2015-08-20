# coding: utf-8

from django.test import TestCase
from django.contrib.auth.models import User


class HomeUnauthenticatedUser(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_get(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/cover.html')


class HomeAuthenticatedUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', password='s3cr3tp4ssw0rd', email='john@doe.com')
        self.client.login(username='john', password='s3cr3tp4ssw0rd')
        self.response = self.client.get('/')

    def test_get(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/home.html')
