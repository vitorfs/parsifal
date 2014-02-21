# coding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('activities.views',
    url(r'^follow/$', 'follow', name='follow'),
    url(r'^unfollow/$', 'unfollow', name='unfollow'),
)