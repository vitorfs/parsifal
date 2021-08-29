from django.urls import path

from parsifal.apps.blog import views

app_name = "blog"

urlpatterns = [
    path("", views.entries, name="entries"),
    path("<slug:slug>/", views.entry, name="entry"),
]
