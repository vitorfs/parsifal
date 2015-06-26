# coding: utf-8

from django.conf.urls import patterns, include, url

urlpatterns = patterns('parsifal.library.views',
    url(r'^$', 'index', name='index'),
    url(r'^new-folder/$', 'new_folder', name='new_folder'),
    url(r'^edit-folder/$', 'edit_folder', name='edit_folder'),
    url(r'^folders/(?P<slug>[-\w]+)/$', 'folder', name='folder'),
)
