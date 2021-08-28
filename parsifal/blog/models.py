from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Entry(models.Model):
    DRAFT = "D"
    HIDDEN = "H"
    PUBLISHED = "P"
    ENTRY_STATUS = (
        (DRAFT, _("Draft")),
        (HIDDEN, _("Hidden")),
        (PUBLISHED, _("Published")),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    content = models.TextField(max_length=4000, null=True, blank=True)
    summary = models.TextField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=10, choices=ENTRY_STATUS)
    start_publication = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="+")

    class Meta:
        verbose_name = _("entry")
        verbose_name_plural = _("entries")

    def __str__(self):
        return self.title
