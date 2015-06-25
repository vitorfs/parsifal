# coding: utf-8

from django.conf.urls import patterns, include, url

urlpatterns = patterns('parsifal.library.views',
    url(r'^$', 'index', name='index'),
    url(r'^add-folder/$', 'add_folder', name='add_folder'),
    url(r'^folders/(?P<slug>[-\w]+)/$', 'folder', name='folder'),
)
