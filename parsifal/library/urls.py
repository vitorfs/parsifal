from django.urls import path

from parsifal.library import views

app_name = "library"

urlpatterns = [
    path("", views.index, name="index"),
    path("list_actions/", views.list_actions, name="list_actions"),
    path("new_folder/", views.new_folder, name="new_folder"),
    path("edit_folder/", views.edit_folder, name="edit_folder"),
    path("folders/<slug:slug>/", views.folder, name="folder"),
    path("new_shared_folder/", views.new_shared_folder, name="new_shared_folder"),
    path("shared/<slug:slug>/", views.shared_folder, name="shared_folder"),
    path("new_document/", views.new_document, name="new_document"),
    path("documents/<int:document_id>/", views.document, name="document"),
    path("move/", views.move, name="move"),
    path("copy/", views.copy, name="copy"),
    path("remove_from_folder/", views.remove_from_folder, name="remove_from_folder"),
    path("delete_documents/", views.delete_documents, name="delete_documents"),
    path("import_bibtex/", views.import_bibtex, name="import_bibtex"),
]
