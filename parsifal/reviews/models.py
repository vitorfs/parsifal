from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
  short_name = models.CharField(max_length=50)
  title = models.CharField(max_length=200)
  description = models.CharField(max_length=500)
  user = models.ForeignKey(User)

  def __unicode__(self):
      return self.short_name

  class Meta:
      verbose_name = "Review"
      verbose_name_plural = "Reviews"