from django.urls import path

from parsifal.reviews.conducting import views

urlpatterns = [
    path("add_source_string/", views.add_source_string, name="add_source_string"),
    path("save_source_string/", views.save_source_string, name="save_source_string"),
    path("remove_source_string/", views.remove_source_string, name="remove_source_string"),
    path("import_base_string/", views.import_base_string, name="import_base_string"),
    path("search_scopus/", views.search_scopus, name="search_scopus"),
    path("search_science_direct/", views.search_science_direct, name="search_science_direct"),
    path("new_article/", views.new_article, name="new_article"),
    path("import/bibtex_file/", views.import_bibtex, name="import_bibtex"),
    path("import/bibtex_raw_content/", views.import_bibtex_raw_content, name="import_bibtex_raw_content"),
    path("source_articles/", views.source_articles, name="source_articles"),
    path("article_details/", views.article_details, name="article_details"),
    path("find_duplicates/", views.find_duplicates, name="find_duplicates"),
    path("resolve_duplicated/", views.resolve_duplicated, name="resolve_duplicated"),
    path("export_results/", views.export_results, name="export_results"),
    path("resolve_all/", views.resolve_all, name="resolve_all"),
    path("save_article_details/", views.save_article_details, name="save_article_details"),
    path("save_quality_assessment/", views.save_quality_assessment, name="save_quality_assessment"),
    path("quality_assessment_detailed/", views.quality_assessment_detailed, name="quality_assessment_detailed"),
    path("quality_assessment_summary/", views.quality_assessment_summary, name="quality_assessment_summary"),
    path(
        "multiple_articles_action/remove/",
        views.multiple_articles_action_remove,
        name="multiple_articles_action_remove",
    ),
    path(
        "multiple_articles_action/accept/",
        views.multiple_articles_action_accept,
        name="multiple_articles_action_accept",
    ),
    path(
        "multiple_articles_action/reject/",
        views.multiple_articles_action_reject,
        name="multiple_articles_action_reject",
    ),
    path(
        "multiple_articles_action/duplicated/",
        views.multiple_articles_action_duplicated,
        name="multiple_articles_action_duplicated",
    ),
    path("save_data_extraction/", views.save_data_extraction, name="save_data_extraction"),
    path("save_data_extraction_status/", views.save_data_extraction_status, name="save_data_extraction_status"),
    path("articles_selection_chart/", views.articles_selection_chart, name="articles_selection_chart"),
    path("articles_per_year/", views.articles_per_year, name="articles_per_year"),
    path("export_data_extraction/", views.export_data_extraction, name="export_data_extraction"),
]
