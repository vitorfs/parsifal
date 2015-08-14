# coding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('parsifal.account_settings.views',
    url(r'^$', 'settings', name='settings'),
    url(r'^profile/$', 'profile', name='profile'),
    url(r'^emails/$', 'emails', name='emails'),
    url(r'^picture/$', 'picture', name='picture'),
    url(r'^password/$', 'password', name='password'),

    url(r'^connections/$', 'connections', name='connections'),
    
    url(r'^mendeley_connection/$', 'mendeley_connection', name='mendeley_connection'),
    url(r'^connect_mendeley/$', 'connect_mendeley', name='connect_mendeley'),
    url(r'^disconnect_mendeley/$', 'disconnect_mendeley', name='disconnect_mendeley'),

    url(r'^dropbox_connection/$', 'dropbox_connection', name='dropbox_connection'),
    url(r'^connect_dropbox/$', 'connect_dropbox', name='connect_dropbox'),
    url(r'^disconnect_dropbox/$', 'disconnect_dropbox', name='disconnect_dropbox'),

    url(r'^upload_picture/$', 'upload_picture', name='upload_picture'),
    url(r'^save_uploaded_picture/$', 'save_uploaded_picture', name='save_uploaded_picture'),
)