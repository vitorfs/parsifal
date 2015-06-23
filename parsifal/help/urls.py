# coding: utf-8

from django.conf.urls import patterns, include, url

urlpatterns = patterns('parsifal.help.views',
    url(r'^$', 'articles', name='articles'),
    url(r'^(?P<slug>[-\w]+)/$', 'article', name='article'),
)
