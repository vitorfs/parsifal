from django.core import mail
from django.test.testcases import TestCase
from django.urls import reverse

from parsifal.apps.activities.constants import ActivityTypes
from parsifal.apps.activities.models import Activity
from parsifal.apps.authentication.tests.factories import UserFactory
from parsifal.apps.invites.constants import InviteStatus
from parsifal.apps.invites.models import Invite
from parsifal.apps.invites.tests.factories import InviteFactory


class TestManageAccessView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.co_author = UserFactory()
        cls.invite = InviteFactory(review__co_authors=[cls.co_author])
        cls.url = reverse(
            "invites:manage_access",
            args=(
                cls.invite.review.author.username,
                cls.invite.review.name,
            ),
        )

    def test_login_required(self):
        response = self.client.get(self.url)
        self.assertEqual(404, response.status_code)

    def test_main_author_required(self):
        self.client.force_login(self.co_author)
        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)

    def test_get_success(self):
        self.client.force_login(self.invite.review.author)
        response = self.client.get(self.url)
        with self.subTest(msg="Test get status code"):
            self.assertEqual(200, response.status_code)

        parts = ("csrfmiddlewaretoken", 'name="invitee"', 'name="invitee_email"', self.invite.get_invitee_email())
        for part in parts:
            with self.subTest(msg="Test response body", part=part):
                self.assertContains(response, part)

    def test_post_success_invitee_email(self):
        data = {
            "invitee_email": "doe.john@example.com",
        }
        self.client.force_login(self.invite.review.author)
        response = self.client.post(self.url, data, follow=True)
        with self.subTest(msg="Test post status code"):
            self.assertEqual(302, response.redirect_chain[0][1])

        with self.subTest(msg="Test post redirect status code"):
            self.assertEqual(200, response.status_code)

        with self.subTest(msg="Test success message"):
            self.assertContains(response, "An invitation was sent to doe.john@example.com.")

        with self.subTest(msg="Test invite created"):
            self.assertTrue(
                Invite.objects.filter(invitee_email="doe.john@example.com", status=InviteStatus.PENDING).exists()
            )

        with self.subTest(msg="Test email sent"):
            self.assertEqual(1, len(mail.outbox))

    def test_post_success_invitee(self):
        contact = UserFactory(email="contact@parsif.al")
        Activity.objects.create(
            from_user=self.invite.review.author, to_user=contact, activity_type=ActivityTypes.FOLLOW
        )

        with self.subTest(msg="Test setup"):
            self.assertFalse(self.invite.review.is_author_or_coauthor(contact))

        data = {
            "invitee": contact.pk,
        }
        self.client.force_login(self.invite.review.author)
        response = self.client.post(self.url, data, follow=True)
        with self.subTest(msg="Test post status code"):
            self.assertEqual(302, response.redirect_chain[0][1])

        with self.subTest(msg="Test post redirect status code"):
            self.assertEqual(200, response.status_code)

        with self.subTest(msg="Test success message"):
            self.assertContains(response, "An invitation was sent to contact@parsif.al.")

        with self.subTest(msg="Test invite created"):
            self.assertTrue(
                Invite.objects.filter(
                    invitee=contact, invitee_email="contact@parsif.al", status=InviteStatus.PENDING
                ).exists()
            )

        with self.subTest(msg="Test email sent"):
            self.assertEqual(1, len(mail.outbox))
