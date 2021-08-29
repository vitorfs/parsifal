from django.urls import path

from parsifal.apps.reviews.planning import views

app_name = "planning"

urlpatterns = [
    path("save_source/", views.save_source, name="save_source"),
    path("remove_source/", views.remove_source_from_review, name="remove_source_from_review"),
    path("suggested_sources/", views.suggested_sources, name="suggested_sources"),
    path("add_suggested_sources/", views.add_suggested_sources, name="add_suggested_sources"),
    path("save_question/", views.save_question, name="save_question"),
    path("save_question_order/", views.save_question_order, name="save_question_order"),
    path("save_picoc/", views.save_picoc, name="save_picoc"),
    path("add_or_edit_question/", views.add_or_edit_question, name="add_or_edit_question"),
    path("remove_question/", views.remove_question, name="remove_question"),
    path("save_objective/", views.save_objective, name="save_objective"),
    path("add_criteria/", views.add_criteria, name="add_criteria"),
    path("remove_criteria/", views.remove_criteria, name="remove_criteria"),
    path("import_pico_keywords/", views.import_pico_keywords, name="import_pico_keywords"),
    path("add_keyword/", views.add_keyword, name="add_keyword"),
    path("edit_keyword/", views.edit_keyword, name="edit_keyword"),
    path("remove_keyword/", views.remove_keyword, name="remove_keyword"),
    path(
        "add_quality_assessment_question/",
        views.add_quality_assessment_question,
        name="add_quality_assessment_question",
    ),
    path(
        "edit_quality_assessment_question/",
        views.edit_quality_assessment_question,
        name="edit_quality_assessment_question",
    ),
    path(
        "save_quality_assessment_question/",
        views.save_quality_assessment_question,
        name="save_quality_assessment_question",
    ),
    path(
        "save_quality_assessment_question_order/",
        views.save_quality_assessment_question_order,
        name="save_quality_assessment_question_order",
    ),
    path(
        "remove_quality_assessment_question/",
        views.remove_quality_assessment_question,
        name="remove_quality_assessment_question",
    ),
    path("add_quality_assessment_answer/", views.add_quality_assessment_answer, name="add_quality_assessment_answer"),
    path(
        "edit_quality_assessment_answer/", views.edit_quality_assessment_answer, name="edit_quality_assessment_answer"
    ),
    path(
        "save_quality_assessment_answer/", views.save_quality_assessment_answer, name="save_quality_assessment_answer"
    ),
    path(
        "remove_quality_assessment_answer/",
        views.remove_quality_assessment_answer,
        name="remove_quality_assessment_answer",
    ),
    path("add_suggested_answer/", views.add_suggested_answer, name="add_suggested_answer"),
    path("add_new_data_extraction_field/", views.add_new_data_extraction_field, name="add_new_data_extraction_field"),
    path("edit_data_extraction_field/", views.edit_data_extraction_field, name="edit_data_extraction_field"),
    path("save_data_extraction_field/", views.save_data_extraction_field, name="save_data_extraction_field"),
    path(
        "save_data_extraction_field_order/",
        views.save_data_extraction_field_order,
        name="save_data_extraction_field_order",
    ),
    path("remove_data_extraction_field/", views.remove_data_extraction_field, name="remove_data_extraction_field"),
    path("calculate_max_score/", views.calculate_max_score, name="calculate_max_score"),
    path("save_cutoff_score/", views.save_cutoff_score, name="save_cutoff_score"),
    path("generate_search_string/", views.generate_search_string, name="generate_search_string"),
    path("save_generic_search_string/", views.save_generic_search_string, name="save_generic_search_string"),
]
