from django.urls import path

from parsifal.reviews.reporting import views

app_name = "reporting"

urlpatterns = [
    path("download_docx/", views.download_docx, name="download_docx"),
]
