import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Source(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Source"
        verbose_name_plural = "Sources"
        ordering = ("name",)

class Question(models.Model):
    QUESTION_TYPES = (
            (u'M', u'Main'),
            (u'S', u'Secondary'),
        )

    question = models.CharField(max_length=500)
    population = models.CharField(max_length=200)
    intervention = models.CharField(max_length=200)
    comparison = models.CharField(max_length=200)
    outcome = models.CharField(max_length=200)
    question_type = models.CharField(max_length=1, choices=QUESTION_TYPES)

    def __unicode__(self):
        return self.question

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions" 

class Review(models.Model):
    short_name = models.CharField(max_length=50) #TODO: Change var name to Name
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    user = models.ForeignKey(User) #TODO: Change var name to Author
    create_date = models.DateTimeField(auto_now_add=True, blank=True)
    last_update = models.DateTimeField()
    co_authors = models.ManyToManyField(User, related_name="co+")
    objective = models.TextField(max_length=1000, null=True)
    questions = models.ManyToManyField(Question)
    sources = models.ManyToManyField(Source)

    def __unicode__(self):
        return self.short_name

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

class ReferenceArticle:
    id = ""
    title = ""
    author = ""
    journal = ""
    year = ""