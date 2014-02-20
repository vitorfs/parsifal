# coding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('activities.views',
    url(r'^follow/(?P<username>[\w-]+)/$', 'follow', name='follow'),
    url(r'^unfollow/(?P<username>[\w-]+)/$', 'unfollow', name='unfollow'),
)