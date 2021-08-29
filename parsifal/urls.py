from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from parsifal.apps.activities import views as activities_views
from parsifal.apps.authentication import views as auth_views
from parsifal.apps.core import views as core_views
from parsifal.apps.reviews import views as reviews_views
from parsifal.apps.reviews.conducting import views as reviews_conducting_views
from parsifal.apps.reviews.planning import views as reviews_planning_views
from parsifal.apps.reviews.reporting import views as reviews_reporting_views
from parsifal.apps.reviews.settings import views as reviews_settings_views

urlpatterns = [
    path("", core_views.home, name="home"),
    path("about/", TemplateView.as_view(template_name="core/about.html"), name="about"),
    path("signup/", auth_views.signup, name="signup"),
    path("signin/", auth_views.signin, name="signin"),
    path("signout/", auth_views.signout, name="signout"),
    path("reset/", auth_views.reset, name="reset"),
    path("reset/<str:uidb64>/<str:token>/", auth_views.reset_confirm, name="password_reset_confirm"),
    path("success/", auth_views.success, name="success"),
    path("reviews/", include("parsifal.apps.reviews.urls", namespace="reviews")),
    path("activity/", include("parsifal.apps.activities.urls", namespace="activities")),
    path("blog/", include("parsifal.apps.blog.urls", namespace="blog")),
    path("help/", include("parsifal.apps.help.urls", namespace="help")),
    path("library/", include("parsifal.apps.library.urls", namespace="library")),
    path("settings/", include("parsifal.apps.account_settings.urls", namespace="settings")),
    path("review_settings/transfer/", reviews_settings_views.transfer, name="transfer_review"),
    path("review_settings/delete/", reviews_settings_views.delete, name="delete_review"),
    path("admin/", admin.site.urls),
    path("sitemap.xml", TemplateView.as_view(template_name="sitemap.xml", content_type="application/xml")),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("<str:username>/following/", activities_views.following, name="following"),
    path("<str:username>/followers/", activities_views.followers, name="followers"),
    # Review URLs
    path("<str:username>/<str:review_name>/", reviews_views.review, name="review"),
    path("<str:username>/<str:review_name>/settings/", reviews_settings_views.settings, name="settings"),
    # Planning Phase
    path("<str:username>/<str:review_name>/planning/", reviews_planning_views.planning, name="planning"),
    path("<str:username>/<str:review_name>/planning/protocol/", reviews_planning_views.protocol, name="protocol"),
    path(
        "<str:username>/<str:review_name>/planning/quality/",
        reviews_planning_views.quality_assessment_checklist,
        name="quality_assessment_checklist",
    ),
    path(
        "<str:username>/<str:review_name>/planning/extraction/",
        reviews_planning_views.data_extraction_form,
        name="data_extraction_form",
    ),
    # Conducting Phase
    path("<str:username>/<str:review_name>/conducting/", reviews_conducting_views.conducting, name="conducting"),
    path(
        "<str:username>/<str:review_name>/conducting/search/",
        reviews_conducting_views.search_studies,
        name="search_studies",
    ),
    path(
        "<str:username>/<str:review_name>/conducting/import/",
        reviews_conducting_views.import_studies,
        name="import_studies",
    ),
    path(
        "<str:username>/<str:review_name>/conducting/studies/",
        reviews_conducting_views.study_selection,
        name="study_selection",
    ),
    path(
        "<str:username>/<str:review_name>/conducting/quality/",
        reviews_conducting_views.quality_assessment,
        name="quality_assessment",
    ),
    path(
        "<str:username>/<str:review_name>/conducting/extraction/",
        reviews_conducting_views.data_extraction,
        name="data_extraction",
    ),
    path(
        "<str:username>/<str:review_name>/conducting/analysis/",
        reviews_conducting_views.data_analysis,
        name="data_analysis",
    ),
    # Reporting Phase
    path(
        "<str:username>/<str:review_name>/reporting/",
        reviews_reporting_views.reporting,
        name="reporting",
    ),
    path(
        "<str:username>/<str:review_name>/reporting/export/",
        reviews_reporting_views.export,
        name="export",
    ),
    path("<str:username>/", reviews_views.reviews, name="reviews"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
