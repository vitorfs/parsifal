# coding: utf-8

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'core.views.home'),
    (r'^signin/$', 'core.views.signin'),
    (r'^signout/$', 'core.views.signout'),
    (r'^news/$', 'core.views.news'),
    (r'^about/$', 'core.views.about'),
    (r'^help/$', 'core.views.help'),
    (r'^users/new/$', 'users.views.new'),
    (r'^settings/$', 'settings.views.settings'),
    (r'^settings/profile/$', 'settings.views.profile'),
    (r'^settings/password/$', 'settings.views.password'),
    (r'^reviews/new/$', 'reviews.views.new'),
    (r'^reviews/add_author/$', 'reviews.views.add_author_to_review'),
    (r'^reviews/remove_author/$', 'reviews.views.remove_author_from_review'),
    (r'^reviews/save_description/$', 'reviews.views.save_description'),
    (r'^reviews/planning/save_source/$', 'reviews.views.save_source'),
    (r'^reviews/planning/remove_source/$', 'reviews.views.remove_source_from_review'),
    (r'^reviews/planning/add_suggested_sources/$', 'reviews.views.add_suggested_sources'),
    (r'^reviews/planning/save_question/$', 'reviews.views.save_question'),
    (r'^reviews/planning/add_question/$', 'reviews.views.add_question'),
    (r'^reviews/planning/remove_question/$', 'reviews.views.remove_question'),
    (r'^reviews/planning/save_objective/$', 'reviews.views.save_objective'),
    (r'^reviews/planning/add_criteria/$', 'reviews.views.add_criteria'),
    (r'^reviews/planning/remove_criteria/$', 'reviews.views.remove_criteria'),
    (r'^reviews/planning/add_synonym/$', 'reviews.views.add_synonym'),
    (r'^reviews/planning/add_new_keyword/$', 'reviews.views.add_new_keyword'),
    (r'^reviews/planning/save_keyword/$', 'reviews.views.save_keyword'),
    (r'^reviews/planning/save_synonym/$', 'reviews.views.save_synonym'),
    (r'^reviews/planning/import_pico_keywords/$', 'reviews.views.import_pico_keywords'),
    (r'^reviews/planning/remove_keyword/$', 'reviews.views.remove_keyword'),
    (r'^(?P<username>[\w-]+)/(?P<review_name>[\w-]+)/$', 'reviews.views.review'),
    (r'^(?P<username>[\w-]+)/(?P<review_name>[\w-]+)/planning/$', 'reviews.views.planning'),
    (r'^(?P<username>[\w-]+)/(?P<review_name>[\w-]+)/conducting/$', 'reviews.views.conducting'),
    (r'^(?P<username>[\w-]+)/(?P<review_name>[\w-]+)/reporting/$', 'reviews.views.reporting'),
    (r'^(?P<username>[\w-]+)/$', 'reviews.views.reviews'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
