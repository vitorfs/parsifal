from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    location = models.CharField(max_length=50)
    url = models.CharField(max_length=50)
    institution = models.CharField(max_length=50)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.get_profile().save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)