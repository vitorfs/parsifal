# coding: utf-8

from django.contrib import admin
from django.template.defaultfilters import slugify

from parsifal.help.models import Article, Category, Media


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'category', 'parent', 'is_active', 'views',]
    list_filter = ['category',]
    search_fields = ['title', 'content',]
    fields = ['title', 'description', 'content', 'references', 'category', 'medias', 'parent', 'is_active',]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.slug = slugify(obj.title)
        obj.save()

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug',]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
