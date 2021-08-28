from django.urls import include, path

from parsifal.reviews import views

app_name = "reviews"

urlpatterns = [
    path("new/", views.new, name="new"),
    path("add_author/", views.add_author_to_review, name="add_author_to_review"),
    path("remove_author/", views.remove_author_from_review, name="remove_author_from_review"),
    path("save_description/", views.save_description, name="save_description"),
    path("leave/", views.leave, name="leave"),
    path("planning/", include("parsifal.reviews.planning.urls", namespace="planning")),
    path("conducting/", include("parsifal.reviews.conducting.urls", namespace="conducting")),
    path("reporting/", include("parsifal.reviews.reporting.urls", namespace="reporting")),
]
