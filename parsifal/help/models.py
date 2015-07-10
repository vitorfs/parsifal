from bs4 import BeautifulSoup

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, null=True)

    class Meta:
        verbose_name = u'Category'
        verbose_name_plural = u'Categories'

    def __unicode__(self):
        return self.name

class Media(models.Model):
    IMAGE = u'image'
    VIDEO = u'video'
    MEDIA_TYPES = (
        (IMAGE, u'Image'),
        (VIDEO, u'Video'),
        )

    name = models.CharField(max_length=255)
    url = models.URLField(max_length=500, null=True, blank=True)
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPES)
    content = models.FileField(upload_to=u'help/', null=True, blank=True)
    content_type = models.CharField(max_length=255, null=True, blank=True)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    class Meta:
        verbose_name = u'Media'
        verbose_name_plural = u'Medias'

class Article(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    content = models.TextField(max_length=4000, null=True, blank=True)
    references = models.TextField(max_length=2000, null=True, blank=True)
    category = models.ForeignKey(Category)
    views = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey(u'Article', null=True, blank=True)
    medias = models.ManyToManyField(Media, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name=u'help_article_creation_user')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, null=True, related_name=u'help_article_update_user')

    class Meta:
        verbose_name = u'Article'
        verbose_name_plural = u'Articles'

    def __unicode__(self):
        return self.title

    def raw_content(self):
        soup = BeautifulSoup(self.content)
        return soup.get_text()
