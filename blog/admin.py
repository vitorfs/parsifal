# coding: utf-8

from django.contrib import admin
from blog.models import Entry

class EntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'start_publication', 'creation_date', 'last_update', 'created_by']
    list_filter = ['status',]
    search_fields = ['title', 'content', 'created_by__username']
    date_hierarchy = 'start_publication'

admin.site.register(Entry, EntryAdmin)