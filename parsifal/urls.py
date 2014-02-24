# coding: utf-8

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'core.views.home'),
    (r'^about/$', 'core.views.about'),
    (r'^help/$', 'core.views.help'),
    (r'^signup/$', 'auth.views.signup'),
    (r'^signin/$', 'auth.views.signin'),
    (r'^signout/$', 'auth.views.signout'),
    url(r'^reviews/', include('reviews.urls', namespace='reviews')),
    url(r'^activity/', include('activities.urls', namespace='activities')),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^settings/', include('settings.urls', namespace='settings')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^(?P<username>[\w-]+)/following/$', 'activities.views.following'),
    (r'^(?P<username>[\w-]+)/followers/$', 'activities.views.followers'),
    (r'^(?P<username>[\w-]+)/(?P<review_name>[\w-]+)/$', 'reviews.views.review'),
    (r'^(?P<username>[\w-]+)/(?P<review_name>[\w-]+)/planning/$', 'reviews.views.planning'),
    (r'^(?P<username>[\w-]+)/(?P<review_name>[\w-]+)/conducting/$', 'reviews.views.conducting'),
    (r'^(?P<username>[\w-]+)/(?P<review_name>[\w-]+)/reporting/$', 'reviews.views.reporting'),
    (r'^(?P<username>[\w-]+)/(?P<review_name>[\w-]+)/settings/$', 'reviews.views.settings'),
    (r'^(?P<username>[\w-]+)/(?P<review_name>[\w-]+)/settings/save/$', 'reviews.views.save_settings'),
    (r'^(?P<username>[\w-]+)/$', 'reviews.views.reviews'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)