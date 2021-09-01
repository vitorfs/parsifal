from django.urls import path

from parsifal.apps.account_settings import views

app_name = "account_settings"

urlpatterns = [
    path("", views.settings, name="settings"),
    path("profile/", views.profile, name="profile"),
    path("emails/", views.emails, name="emails"),
    path("picture/", views.picture, name="picture"),
    path("password/", views.password, name="password"),
    path("upload_picture/", views.upload_picture, name="upload_picture"),
    path("save_uploaded_picture/", views.save_uploaded_picture, name="save_uploaded_picture"),
]
