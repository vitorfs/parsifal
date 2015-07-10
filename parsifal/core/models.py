from django.db import models


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
    content = models.FileField(upload_to=u'site/', null=True, blank=True)
    content_type = models.CharField(max_length=255, null=True, blank=True)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    class Meta:
        verbose_name = u'Media'
        verbose_name_plural = u'Medias'

    def __unicode__(self):
        return self.name
        