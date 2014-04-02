# coding: utf-8

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'core.views.home', name='home'),
    url(r'^about/$', 'core.views.about', name='about'),
    url(r'^help/$', 'core.views.help', name='help'),
    url(r'^support/$', 'core.views.support', name='support'),
    url(r'^explore/$', 'core.views.explore', name='explore'),
    url(r'^signup/$', 'auth.views.signup', name='signup'),
    url(r'^signin/$', 'auth.views.signin', name='signin'),
    url(r'^signout/$', 'auth.views.signout', name='signout'),
    url(r'^reset/$', 'auth.views.reset', name='reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'auth.views.reset_confirm', name='password_reset_confirm'),
    url(r'^success/$', 'auth.views.success', name='success'),
    url(r'^reviews/', include('reviews.urls', namespace='reviews')),
    url(r'^activity/', include('activities.urls', namespace='activities')),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^settings/', include('settings.urls', namespace='settings')),
    url(r'^review_settings/save/$', 'reviews.settings.views.save_settings', name='save_settings'),
    url(r'^review_settings/transfer/$', 'reviews.settings.views.transfer', name='transfer_review'),
    url(r'^review_settings/delete/$', 'reviews.settings.views.delete', name='delete_review'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<username>[^/]+)/following/$', 'activities.views.following', name='following'),
    url(r'^(?P<username>[^/]+)/followers/$', 'activities.views.followers', name='followers'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/$', 'reviews.views.review', name='review'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/planning/$', 'reviews.planning.views.planning', name='planning'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/conducting/$', 'reviews.conducting.views.conducting', name='conducting'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/conducting/search/$', 'reviews.conducting.views.search_string', name='search_string'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/conducting/studies/$', 'reviews.conducting.views.study_selection', name='study_selection'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/conducting/quality/$', 'reviews.conducting.views.quality_assessment', name='quality_assessment'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/conducting/extraction/$', 'reviews.conducting.views.data_extraction', name='data_extraction'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/reporting/$', 'reviews.reporting.views.reporting', name='reporting'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/settings/$', 'reviews.settings.views.settings', name='settings'),
    url(r'^(?P<username>[^/]+)/$', 'reviews.views.reviews', name='reviews'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)