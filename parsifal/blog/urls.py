# coding: utf-8

from django.conf.urls import patterns, include, url

urlpatterns = patterns('parsifal.blog.views',
    url(r'^$', 'entries', name='entries'),
    url(r'^(?P<slug>[-\w]+)/$', 'entry', name='entry'),
)
