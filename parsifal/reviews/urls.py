# coding: utf-8

from django.conf.urls import patterns, include, url


urlpatterns = patterns('parsifal.reviews.views',
    url(r'^new/$', 'new', name='new'),
    url(r'^add_author/$', 'add_author_to_review', name='add_author_to_review'),
    url(r'^remove_author/$', 'remove_author_from_review', name='remove_author_from_review'),
    url(r'^save_description/$', 'save_description', name='save_description'),
    url(r'^leave/$', 'leave', name='leave'),
    url(r'^planning/', include('parsifal.reviews.planning.urls', namespace='planning')),
    url(r'^conducting/', include('parsifal.reviews.conducting.urls', namespace='conducting')),
    url(r'^reporting/', include('parsifal.reviews.reporting.urls', namespace='reporting')),
)
