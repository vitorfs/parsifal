# coding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('parsifal.activities.views',
    url(r'^follow/$', 'follow', name='follow'),
    url(r'^unfollow/$', 'unfollow', name='unfollow'),
    url(r'^update_followers_count/$', 'update_followers_count', name='update_followers_count'),
)