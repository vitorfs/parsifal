from django.urls import path

from parsifal.blog import views

urlpatterns = [
    path("", views.entries, name="entries"),
    path("<slug:slug>/", views.entry, name="entry"),
]
