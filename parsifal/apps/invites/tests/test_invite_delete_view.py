from django.test.testcases import TestCase
from django.urls import reverse

from parsifal.apps.authentication.tests.factories import UserFactory
from parsifal.apps.invites.constants import InviteStatus
from parsifal.apps.invites.models import Invite
from parsifal.apps.invites.tests.factories import InviteFactory
from parsifal.utils.test import login_redirect_url


class TestInviteDeleteView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.invite = InviteFactory(invitee_email="invitee@parsif.al")
        cls.co_author = UserFactory()
        cls.invite.review.co_authors.add(cls.co_author)
        cls.url = reverse(
            "invites:invite_delete",
            args=(
                cls.invite.review.author.username,
                cls.invite.review.name,
                cls.invite.pk,
            ),
        )

    def test_login_required(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, login_redirect_url(self.url))

    def test_main_author_required(self):
        self.client.force_login(self.co_author)
        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)

    def test_get_success(self):
        self.client.force_login(self.invite.review.author)

        response = self.client.get(self.url)

        with self.subTest(msg="Test get status code"):
            self.assertEqual(200, response.status_code)

        with self.subTest(msg="Test response body"):
            self.assertContains(
                response, "Are you sure you want to delete the invite sent to <strong>invitee@parsif.al</strong>"
            )

    def test_post_success(self):
        self.client.force_login(self.invite.review.author)
        response = self.client.post(self.url, follow=True)
        with self.subTest(msg="Test post status code"):
            self.assertEqual(302, response.redirect_chain[0][1])

        with self.subTest(msg="Test post redirect status code"):
            self.assertEqual(200, response.status_code)

        with self.subTest(msg="Test success message"):
            self.assertContains(response, "The invitation was removed with success.")

        with self.subTest(msg="Test invite removed"):
            self.assertFalse(Invite.objects.filter(invitee_email="invitee@parsif.al").exists())

    def test_post_fail(self):
        self.invite.status = InviteStatus.ACCEPTED
        self.invite.save()
        self.client.force_login(self.invite.review.author)
        response = self.client.post(self.url)

        with self.subTest(msg="Test post not found status code"):
            self.assertEqual(404, response.status_code)

        with self.subTest(msg="Test not invite removed"):
            self.assertTrue(Invite.objects.filter(invitee_email="invitee@parsif.al").exists())
