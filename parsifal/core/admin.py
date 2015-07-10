# coding: utf-8

from django.contrib import admin

from parsifal.core.models import Media


class MediaAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'media_type', 'content_type', 'width', 'height']
    list_filter = ['media_type',]
    search_fields = ['name',]
    fields = ['name', 'url', 'media_type', 'content', 'content_type', 'width', 'height']

admin.site.register(Media, MediaAdmin)
