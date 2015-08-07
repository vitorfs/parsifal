# coding: utf-8

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'parsifal.core.views.home', name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='core/about.html'), name='about'),
    url(r'^signup/$', 'parsifal.authentication.views.signup', name='signup'),
    url(r'^signin/$', 'parsifal.authentication.views.signin', name='signin'),
    url(r'^signout/$', 'parsifal.authentication.views.signout', name='signout'),
    url(r'^reset/$', 'parsifal.authentication.views.reset', name='reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'parsifal.authentication.views.reset_confirm', name='password_reset_confirm'),
    url(r'^success/$', 'parsifal.authentication.views.success', name='success'),
    url(r'^reviews/', include('parsifal.reviews.urls', namespace='reviews')),
    url(r'^activity/', include('parsifal.activities.urls', namespace='activities')),
    url(r'^blog/', include('parsifal.blog.urls', namespace='blog')),
    url(r'^help/', include('parsifal.help.urls', namespace='help')),
    url(r'^library/', include('parsifal.library.urls', namespace='library')),
    url(r'^settings/', include('parsifal.account_settings.urls', namespace='settings')),
    url(r'^review_settings/transfer/$', 'parsifal.reviews.settings.views.transfer', name='transfer_review'),
    url(r'^review_settings/delete/$', 'parsifal.reviews.settings.views.delete', name='delete_review'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sitemap.xml$', TemplateView.as_view(template_name='sitemap.xml', content_type='application/xml')),
    url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^(?P<username>[^/]+)/following/$', 'parsifal.activities.views.following', name='following'),
    url(r'^(?P<username>[^/]+)/followers/$', 'parsifal.activities.views.followers', name='followers'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/$', 'parsifal.reviews.views.review', name='review'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/planning/$', 'parsifal.reviews.planning.views.planning', name='planning'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/planning/protocol/$', 'parsifal.reviews.planning.views.protocol', name='protocol'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/planning/quality/$', 'parsifal.reviews.planning.views.quality_assessment_checklist', name='quality_assessment_checklist'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/planning/extraction/$', 'parsifal.reviews.planning.views.data_extraction_form', name='data_extraction_form'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/conducting/$', 'parsifal.reviews.conducting.views.conducting', name='conducting'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/conducting/search/$', 'parsifal.reviews.conducting.views.search_studies', name='search_studies'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/conducting/import/$', 'parsifal.reviews.conducting.views.import_studies', name='import_studies'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/conducting/studies/$', 'parsifal.reviews.conducting.views.study_selection', name='study_selection'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/conducting/quality/$', 'parsifal.reviews.conducting.views.quality_assessment', name='quality_assessment'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/conducting/extraction/$', 'parsifal.reviews.conducting.views.data_extraction', name='data_extraction'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/conducting/analysis/$', 'parsifal.reviews.conducting.views.data_analysis', name='data_analysis'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/reporting/$', 'parsifal.reviews.reporting.views.reporting', name='reporting'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/settings/$', 'parsifal.reviews.settings.views.settings', name='settings'),
    url(r'^(?P<username>[^/]+)/$', 'parsifal.reviews.views.reviews', name='reviews'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)