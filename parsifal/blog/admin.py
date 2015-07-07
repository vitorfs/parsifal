# coding: utf-8

from django.contrib import admin
from django.template.defaultfilters import slugify

from parsifal.blog.models import Entry


class EntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'summary', 'creation_date', 'last_update', 'created_by', 'edited_by']
    list_filter = ['status',]
    search_fields = ['title', 'content', 'created_by__username']
    date_hierarchy = 'start_publication'
    fields = ['title', 'content', 'summary', 'status', 'start_publication']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
            obj.save()
        else:
            obj.edited_by = request.user
        slug_str = "%s %s" % (obj.pk, obj.title.lower()) 
        obj.slug = slugify(slug_str)
        obj.save()

admin.site.register(Entry, EntryAdmin)