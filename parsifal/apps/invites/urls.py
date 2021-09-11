from django.urls import path

from parsifal.apps.invites import views

app_name = "invites"

urlpatterns = [
    path("", views.ManageAccessView.as_view(), name="manage_access"),
    path("<int:invite_id>/delete/", views.InviteDeleteView.as_view(), name="invite_delete"),
]
