from django.test.testcases import TestCase

from parsifal.apps.authentication.tests.factories import UserFactory
from parsifal.apps.invites.constants import InviteStatus
from parsifal.apps.invites.tests.factories import InviteFactory


class TestInviteModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.invite = InviteFactory(
            review__name="test-review",
            invitee_email="invitee@parsif.al",
            status=InviteStatus.PENDING,
        )

    def test_setup(self):
        self.assertIsNone(self.invite.date_answered)

    def test_is_pending(self):
        self.assertTrue(self.invite.is_pending)

    def test_accept_invalid(self):
        with self.assertRaises(AssertionError):
            self.invite.accept()

    def test_accept_user_param_success(self):
        invitee = UserFactory()
        self.invite.accept(invitee)

        with self.subTest(msg="Test status"):
            self.assertEqual(InviteStatus.ACCEPTED, self.invite.status)

        with self.subTest(msg="Test invitee assigned"):
            self.assertEqual(invitee, self.invite.invitee)

        with self.subTest(msg="Test co-author added"):
            self.assertTrue(self.invite.review.co_authors.filter(pk=invitee.pk).exists())

        with self.subTest(msg="Test date answered"):
            self.assertIsNotNone(self.invite.date_answered)

    def test_accept_without_user_param_success(self):
        invitee = UserFactory()
        self.invite.invitee = invitee
        self.invite.save()

        self.invite.accept()

        with self.subTest(msg="Test status"):
            self.assertEqual(InviteStatus.ACCEPTED, self.invite.status)

        with self.subTest(msg="Test invitee assigned"):
            self.assertEqual(invitee, self.invite.invitee)

        with self.subTest(msg="Test co-author added"):
            self.assertTrue(self.invite.review.co_authors.filter(pk=invitee.pk).exists())

        with self.subTest(msg="Test date answered"):
            self.assertIsNotNone(self.invite.date_answered)

    def test_str(self):
        expected = "test-review - invitee@parsif.al - pending"
        actual = str(self.invite)
        self.assertEqual(expected, actual)

    def test_get_absolute_url(self):
        expected = f"/invites/{self.invite.code}/"
        actual = self.invite.get_absolute_url()
        self.assertEqual(expected, actual)

    def test_get_invitee_email(self):
        self.assertEqual("invitee@parsif.al", self.invite.get_invitee_email())

    def test_get_invitee_email_with_invitee_instance(self):
        user = UserFactory(email="invitee2@parsif.al")
        self.invite.invitee = user
        self.invite.save()

        with self.subTest(msg="Test setup"):
            self.assertEqual("invitee@parsif.al", self.invite.invitee_email)
            self.assertEqual("invitee2@parsif.al", self.invite.invitee.email)

        with self.subTest(msg="Test get_invitee_email"):
            self.assertEqual("invitee2@parsif.al", self.invite.get_invitee_email())
