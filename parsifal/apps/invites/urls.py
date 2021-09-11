from django.urls import path

from parsifal.apps.invites import views

app_name = "invites"

urlpatterns = [
    path("", views.ManageAccessView.as_view(), name="manage_access"),
    path("<int:invite_id>/<uuid:code>/", views.InviteDetail.as_view(), name="invite_detail"),
]
