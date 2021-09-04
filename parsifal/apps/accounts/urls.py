from django.urls import path

from parsifal.apps.accounts import views

app_name = "accounts"

urlpatterns = [
    path("", views.SettingsRedirectView.as_view(), name="settings"),
    path("profile/", views.UpdateProfileView.as_view(), name="profile"),
    path("emails/", views.UpdateEmailsView.as_view(), name="emails"),
    path("picture/", views.PictureView.as_view(), name="picture"),
    path("upload_picture/", views.upload_picture, name="upload_picture"),
    path("save_uploaded_picture/", views.save_uploaded_picture, name="save_uploaded_picture"),
]
