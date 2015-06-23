# coding: utf-8

import datetime

from django.contrib import admin
from django.template.defaultfilters import slugify

from parsifal.help.models import Article, Category


class ArticleAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
