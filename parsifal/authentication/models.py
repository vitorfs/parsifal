import os.path
try:
    import cPickle as pickle
except:
    import pickle
from mendeley import DefaultStateGenerator
from mendeley.session import MendeleySession
from mendeley.auth import MendeleyAuthorizationCodeAuthenticator, handle_text_response
from oauthlib.oauth2 import TokenExpiredError
from requests_oauthlib import OAuth2Session
from dropbox.client import DropboxClient

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.conf import settings as django_settings

from parsifal.activities.models import Activity
from parsifal.reviews.models import Review


class Profile(models.Model):
    user = models.OneToOneField(User)
    public_email = models.EmailField(null=True, blank=True)
    location = models.CharField(max_length=50)
    url = models.CharField(max_length=50)
    institution = models.CharField(max_length=50)
    mendeley_token = models.CharField(max_length=2000, null=True, blank=True)
    dropbox_token = models.CharField(max_length=2000, null=True, blank=True)

    class Meta:
        db_table = 'auth_profile'

    def set_mendeley_token(self, value):
        self.mendeley_token = pickle.dumps(value)

    def get_mendeley_token(self):
        try:
            return pickle.loads(str(self.mendeley_token))
        except Exception, e:
            return None

    def get_mendeley_session(self):
        mendeley = django_settings.MENDELEY
        token = self.get_mendeley_token()
        mendeley_session = None
        if token:
            mendeley_session = MendeleySession(mendeley, token)
            try:
                mendeley_session.profiles.me
            except TokenExpiredError, e:
                authenticator = MendeleyAuthorizationCodeAuthenticator(mendeley, DefaultStateGenerator.generate_state())
                oauth = OAuth2Session(client=authenticator.client, redirect_uri=mendeley.redirect_uri, scope=['all'])
                oauth.compliance_hook['access_token_response'] = [handle_text_response]
                token = oauth.refresh_token(authenticator.token_url, auth=authenticator.auth, refresh_token=token['refresh_token'])
                self.set_mendeley_token(token)
                self.user.save()
                mendeley_session = MendeleySession(mendeley, token)
            except Exception, e:
                pass
        return mendeley_session

    def get_mendeley_profile(self):
        mendeley_session = self.get_mendeley_session()
        mendeley_profile = None
        if mendeley_session:
            mendeley_profile = mendeley_session.profiles.me
        return mendeley_profile

    def get_dropbox_profile(self):
        dropbox_profile = None
        if self.dropbox_token is not None:
            client = DropboxClient(self.dropbox_token)
            try:
                dropbox_profile = client.account_info()
            except Exception, e:
                pass
        return dropbox_profile

    def get_url(self):
        url = self.url
        if "http://" not in self.url and "https://" not in self.url and len(self.url) > 0:
            url = "http://" + str(self.url)
        return url 

    def get_picture(self):
        no_picture = django_settings.STATIC_URL + 'img/user.png'
        try:
            filename = django_settings.MEDIA_ROOT + '/profile_pictures/' + self.user.username + '.jpg'
            picture_url = django_settings.MEDIA_URL + 'profile_pictures/' + self.user.username + '.jpg'
            if os.path.isfile(filename):
                return picture_url
            else:
                return no_picture
        except Exception, e:
            return no_picture

    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:
            return self.user.username

    def get_followers(self):
        activities = Activity.objects.filter(to_user__pk=self.pk, activity_type=Activity.FOLLOW)
        followers = []
        for activity in activities:
            followers.append(activity.from_user)
        return followers

    def get_followers_count(self):
        followers_count = Activity.objects.filter(to_user__pk=self.pk, activity_type=Activity.FOLLOW).count()
        return followers_count

    def get_following(self):
        activities = Activity.objects.filter(from_user__pk=self.pk, activity_type=Activity.FOLLOW)
        following = []
        for activity in activities:
            following.append(activity.to_user)
        return following

    def get_following_count(self):
        following_count = Activity.objects.filter(from_user__pk=self.pk, activity_type=Activity.FOLLOW).count()
        return following_count

    def get_reviews(self):
        user_reviews = []
        author_reviews = Review.objects.filter(author=self.user)
        co_author_reviews = Review.objects.filter(co_authors=self.user)
        for r in author_reviews: user_reviews.append(r)
        for r in co_author_reviews: user_reviews.append(r)
        user_reviews.sort(key=lambda r: r.last_update, reverse=True)
        return user_reviews

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
