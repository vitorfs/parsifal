# coding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('parsifal_settings.views',
    url(r'^$', 'settings', name='settings'),
    url(r'^profile/$', 'profile', name='profile'),
    url(r'^picture/$', 'picture', name='picture'),
    url(r'^password/$', 'password', name='password'),
    url(r'^connections/$', 'connections', name='connections'),
    url(r'^connect_mendeley/$', 'connect_mendeley', name='connect_mendeley'),
    url(r'^disconnect_mendeley/$', 'disconnect_mendeley', name='disconnect_mendeley'),
    url(r'^upload_picture/$', 'upload_picture', name='upload_picture'),
    url(r'^save_uploaded_picture/$', 'save_uploaded_picture', name='save_uploaded_picture'),
)