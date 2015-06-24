# coding: utf-8

from django.conf.urls import patterns, include, url

urlpatterns = patterns('parsifal.library.views',
    url(r'^$', 'index', name='index'),
)
