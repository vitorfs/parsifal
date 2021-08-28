from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from bs4 import BeautifulSoup

from parsifal.core.models import Media


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, null=True)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    content = models.TextField(max_length=4000, null=True, blank=True)
    references = models.TextField(max_length=2000, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey("Article", on_delete=models.CASCADE, null=True, blank=True)
    medias = models.ManyToManyField(Media, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="help_article_creation_user")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="help_article_update_user")

    class Meta:
        verbose_name = _("article")
        verbose_name_plural = _("articles")

    def __str__(self):
        return self.title

    def raw_content(self):
        soup = BeautifulSoup(self.content)
        return soup.get_text()
