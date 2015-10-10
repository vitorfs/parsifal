# coding: utf-8

from django.conf.urls import patterns, include, url

urlpatterns = patterns('parsifal.library.views',
    url(r'^$', 'index', name='index'),
    url(r'^list_actions/$', 'list_actions', name='list_actions'),
    url(r'^new_folder/$', 'new_folder', name='new_folder'),
    url(r'^edit_folder/$', 'edit_folder', name='edit_folder'),
    url(r'^folders/(?P<slug>[-\w]+)/$', 'folder', name='folder'),
    url(r'^new_shared_folder/$', 'new_shared_folder', name='new_shared_folder'),
    url(r'^shared/(?P<slug>[-\w]+)/$', 'shared_folder', name='shared_folder'),
    url(r'^new_document/$', 'new_document', name='new_document'),
    url(r'^documents/(?P<document_id>\d+)/$', 'document', name='document'),
    url(r'^move/$', 'move', name='move'),
    url(r'^copy/$', 'copy', name='copy'),
    url(r'^remove_from_folder/$', 'remove_from_folder', name='remove_from_folder'),
    url(r'^delete_documents/$', 'delete_documents', name='delete_documents'),
    url(r'^import_bibtex/$', 'import_bibtex', name='import_bibtex'),
)
