from django.contrib import admin

from parsifal.apps.reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "title",
        "description",
        "author",
        "create_date",
        "last_update",
    )
    search_fields = ("name", "title", "description")
    filter_horizontal = ("co_authors",)
    fields = [
        "name",
        "title",
        "description",
        "author",
        "objective",
        "sources",
        "status",
        "co_authors",
        "quality_assessment_cutoff_score",
        "population",
        "intervention",
        "comparison",
        "outcome",
        "context",
    ]
    raw_id_fields = ("author", "co_authors")
