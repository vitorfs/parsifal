from django.urls import include, path

from parsifal.apps.reviews import views

app_name = "reviews"

urlpatterns = [
    path("new/", views.CreateReviewView.as_view(), name="new"),
    path("remove_author/", views.remove_author_from_review, name="remove_author_from_review"),
    path("save_description/", views.save_description, name="save_description"),
    path("leave/", views.leave, name="leave"),
    path("planning/", include("parsifal.apps.reviews.planning.urls", namespace="planning")),
    path("conducting/", include("parsifal.apps.reviews.conducting.urls", namespace="conducting")),
    path("reporting/", include("parsifal.apps.reviews.reporting.urls", namespace="reporting")),
]
