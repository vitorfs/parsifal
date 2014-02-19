# coding: utf-8

import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Entry(models.Model):
    ENTRY_STATUS = (
        (u'D', u'Draft'),
        (u'H', u'Hidden'),
        (u'P', u'Published'),
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    content = models.TextField(max_length=2000)
    status = models.CharField(max_length=10, choices=ENTRY_STATUS)
    start_publication = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User)
    creation_date = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(blank=True, null=True)
    edited_by = models.ForeignKey(User, null=True, blank=True, related_name="+")

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "Entry"
        verbose_name_plural = "Entries"