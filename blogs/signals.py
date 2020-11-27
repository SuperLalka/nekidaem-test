from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from blogs import models


@receiver(post_save, sender=User)
def create_extending_user(instance, **kwargs):
    if not models.ExtendingUser.objects.filter(user=instance).exists():
        extending_user = models.ExtendingUser.objects.create(user=instance)
        extending_user.save()
        user_blog = models.Blog.objects.create(user=extending_user)
        user_blog.save()
