# coding: utf-8

from django.conf.urls import patterns, include, url


urlpatterns = patterns('parsifal.reviews.conducting.views',
    url(r'^add_source_string/$', 'add_source_string', name='add_source_string'),
    url(r'^save_source_string/$', 'save_source_string', name='save_source_string'),
    url(r'^remove_source_string/$', 'remove_source_string', name='remove_source_string'),
    url(r'^import_base_string/$', 'import_base_string', name='import_base_string'),
    url(r'^search_scopus/$', 'search_scopus', name='search_scopus'),
    url(r'^search_science_direct/$', 'search_science_direct', name='search_science_direct'),
    url(r'^new_article/$', 'new_article', name='new_article'),
    url(r'^import/bibtex_file/$', 'import_bibtex', name='import_bibtex'),
    url(r'^import/bibtex_raw_content/$', 'import_bibtex_raw_content', name='import_bibtex_raw_content'),
    url(r'^source_articles/$', 'source_articles', name='source_articles'),
    url(r'^article_details/$', 'article_details', name='article_details'),
    url(r'^find_duplicates/$', 'find_duplicates', name='find_duplicates'),
    url(r'^resolve_duplicated/$', 'resolve_duplicated', name='resolve_duplicated'),
    url(r'^export_results/$', 'export_results', name='export_results'),
    url(r'^resolve_all/$', 'resolve_all', name='resolve_all'),
    url(r'^save_article_details/$', 'save_article_details', name='save_article_details'),
    url(r'^save_quality_assessment/$', 'save_quality_assessment', name='save_quality_assessment'),
    url(r'^quality_assessment_detailed/$', 'quality_assessment_detailed', name='quality_assessment_detailed'),
    url(r'^quality_assessment_summary/$', 'quality_assessment_summary', name='quality_assessment_summary'),
    url(r'^multiple_articles_action/remove/$', 'multiple_articles_action_remove', name='multiple_articles_action_remove'),
    url(r'^multiple_articles_action/accept/$', 'multiple_articles_action_accept', name='multiple_articles_action_accept'),
    url(r'^multiple_articles_action/reject/$', 'multiple_articles_action_reject', name='multiple_articles_action_reject'),
    url(r'^multiple_articles_action/duplicated/$', 'multiple_articles_action_duplicated', name='multiple_articles_action_duplicated'),
    #url(r'^articles/upload/$', 'articles_upload', name='articles_upload'),
    url(r'^save_data_extraction/$', 'save_data_extraction', name='save_data_extraction'),
    url(r'^save_data_extraction_status/$', 'save_data_extraction_status', name='save_data_extraction_status'),
    url(r'^articles_selection_chart/$', 'articles_selection_chart', name='articles_selection_chart'),
    url(r'^articles_per_year/$', 'articles_per_year', name='articles_per_year'),
    url(r'^export_data_extraction/$', 'export_data_extraction', name='export_data_extraction')
)
