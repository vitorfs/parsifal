from django.urls import path

from parsifal.account_settings import views

urlpatterns = [
    path("", views.settings, name="settings"),
    path("profile/", views.profile, name="profile"),
    path("emails/", views.emails, name="emails"),
    path("picture/", views.picture, name="picture"),
    path("password/", views.password, name="password"),
    path("connections/", views.connections, name="connections"),
    path("mendeley_connection/", views.mendeley_connection, name="mendeley_connection"),
    path("connect_mendeley/", views.connect_mendeley, name="connect_mendeley"),
    path("disconnect_mendeley/", views.disconnect_mendeley, name="disconnect_mendeley"),
    path("dropbox_connection/", views.dropbox_connection, name="dropbox_connection"),
    path("connect_dropbox/", views.connect_dropbox, name="connect_dropbox"),
    path("disconnect_dropbox/", views.disconnect_dropbox, name="disconnect_dropbox"),
    path("upload_picture/", views.upload_picture, name="upload_picture"),
    path("save_uploaded_picture/", views.save_uploaded_picture, name="save_uploaded_picture"),
]
