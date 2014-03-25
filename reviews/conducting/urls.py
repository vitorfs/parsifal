# coding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('reviews.conducting.views',
    url(r'^generate_search_string/$', 'generate_search_string', name='generate_search_string'),
    url(r'^save_generic_search_string/$', 'save_generic_search_string', name='save_generic_search_string'),
    url(r'^import_bibtex/$', 'import_bibtex', name='import_bibtex'),
    url(r'^source_articles/$', 'source_articles', name='source_articles'),
    url(r'^article_details/$', 'article_details', name='article_details'),
    url(r'^find_duplicates/$', 'find_duplicates', name='find_duplicates'),
    url(r'^resolve_duplicated/$', 'resolve_duplicated', name='resolve_duplicated'),
    url(r'^resolve_all/$', 'resolve_all', name='resolve_all'),
    url(r'^save_article_details/$', 'save_article_details', name='save_article_details'),
    url(r'^save_quality_assessment/$', 'save_quality_assessment', name='save_quality_assessment'),
    url(r'^quality_assessment_detailed/$', 'quality_assessment_detailed', name='quality_assessment_detailed'),
    url(r'^quality_assessment_summary/$', 'quality_assessment_summary', name='quality_assessment_summary'),
    url(r'^multiple_articles_action/remove/$', 'multiple_articles_action_remove', name='multiple_articles_action_remove'),
    url(r'^multiple_articles_action/accept/$', 'multiple_articles_action_accept', name='multiple_articles_action_accept'),
    url(r'^multiple_articles_action/reject/$', 'multiple_articles_action_reject', name='multiple_articles_action_reject'),
    url(r'^articles/order_by/$', 'articles_order_by', name='articles_order_by'),
    url(r'^save_data_extraction/$', 'save_data_extraction', name='save_data_extraction'),
)