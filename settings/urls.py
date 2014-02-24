# coding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('settings.views',
    url(r'^$', 'settings', name='settings'),
    url(r'^profile/$', 'profile', name='profile'),
    url(r'^password/$', 'password', name='password'),
)