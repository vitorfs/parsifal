# coding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('reviews.conducting.views',
    url(r'^generate_search_string/$', 'generate_search_string', name='generate_search_string'),
    url(r'^save_generic_search_string/$', 'save_generic_search_string', name='save_generic_search_string'),
    url(r'^import_bibtex/$', 'import_bibtex', name='import_bibtex'),
    url(r'^source_articles/$', 'source_articles', name='source_articles'),
    url(r'^article_details/$', 'article_details', name='article_details'),
    url(r'^save_article_details/$', 'save_article_details', name='save_article_details'),
    url(r'^search_string/$', 'search_string', name='search_string'),
    url(r'^study_selection/$', 'study_selection', name='study_selection'),
    url(r'^quality_assessment/$', 'quality_assessment', name='quality_assessment'),
    url(r'^data_extraction/$', 'data_extraction', name='data_extraction'),
)