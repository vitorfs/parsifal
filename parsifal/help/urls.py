from django.urls import path

from parsifal.help import views

urlpatterns = [
    path("", views.articles, name="articles"),
    path("search/", views.search, name="search"),
    path("<slug:slug>/", views.article, name="article"),
]
