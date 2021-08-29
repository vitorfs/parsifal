from django.urls import path

from parsifal.apps.activities import views

app_name = "activities"

urlpatterns = [
    path("follow/", views.follow, name="follow"),
    path("unfollow/", views.unfollow, name="unfollow"),
    path("update_followers_count/", views.update_followers_count, name="update_followers_count"),
]
