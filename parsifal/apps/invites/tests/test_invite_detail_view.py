from django.test.testcases import TestCase
from django.urls import reverse

from parsifal.apps.authentication.tests.factories import UserFactory
from parsifal.apps.invites.constants import InviteStatus
from parsifal.apps.invites.tests.factories import InviteFactory


class TestInviteDetailView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.invite = InviteFactory()
        cls.url = reverse("invite", args=(cls.invite.code,))
        cls.login_url = reverse("login")
        cls.signup_url = reverse("signup")
        cls.accept_url = reverse("accept_user_invite", args=(cls.invite.pk,))
        cls.reject_url = reverse("reject_user_invite", args=(cls.invite.pk,))

    def test_get_invitee_email(self):
        response = self.client.get(self.url)

        with self.subTest(msg="Test get status code"):
            self.assertEqual(200, response.status_code)

        with self.subTest(msg="Test response body"):
            self.assertContains(response, "To accept the invitation, you must create an account on Parsifal")
            self.assertContains(response, self.signup_url)
            self.assertNotContains(response, self.login_url)
            self.assertNotContains(response, self.accept_url)
            self.assertNotContains(response, self.reject_url)

    def test_get_invitee(self):
        user = UserFactory()
        self.invite.invitee = user
        self.invite.save()
        response = self.client.get(self.url)

        with self.subTest(msg="Test get status code"):
            self.assertEqual(200, response.status_code)

        with self.subTest(msg="Test response body"):
            self.assertContains(response, "To accept the invitation, you must log in to your account")
            self.assertNotContains(response, self.signup_url)
            self.assertContains(response, self.login_url)
            self.assertNotContains(response, self.accept_url)
            self.assertNotContains(response, self.reject_url)

    def test_get_invitee_authenticated(self):
        user = UserFactory(username="invitee_user")
        self.invite.invitee = user
        self.invite.save()

        self.client.force_login(user)
        response = self.client.get(self.url)

        with self.subTest(msg="Test get status code"):
            self.assertEqual(200, response.status_code)

        with self.subTest(msg="Test response body"):
            self.assertContains(response, "You are currently logged in as <strong>invitee_user</strong>")
            self.assertNotContains(response, "To accept the invitation, you must log in to your account")
            self.assertNotContains(response, self.signup_url)
            self.assertNotContains(response, self.login_url)
            self.assertContains(response, self.accept_url)
            self.assertContains(response, self.reject_url)

    def test_cant_access_accepted_invites(self):
        self.invite.status = InviteStatus.ACCEPTED
        self.invite.save()
        response = self.client.get(self.url)
        self.assertEqual(404, response.status_code)

    def test_cant_access_rejected_invites(self):
        self.invite.status = InviteStatus.REJECTED
        self.invite.save()
        response = self.client.get(self.url)
        self.assertEqual(404, response.status_code)
