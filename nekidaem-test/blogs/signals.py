from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from blogs import models
from nekidaem_test import settings


@receiver(post_save, sender=User)
def create_extending_user(instance, **kwargs):
    if not models.ExtendingUser.objects.filter(user=instance).exists():
        extending_user = models.ExtendingUser.objects.create(user=instance)
        extending_user.save()
        user_blog = models.Blog.objects.create(user=extending_user)
        user_blog.save()


@receiver(post_save, sender=models.Post)
def inform_the_subscriber(instance, **kwargs):
    list_of_subscriptions = list(models.ExtendingUser.objects.filter(
        subscribed_to=instance.blog))
    for extendinguser in list_of_subscriptions:
        message = f"Hello {extendinguser.user.username}, " \
                  f"a new post {instance.header} has appeared on the {instance.blog} blog, " \
                  f"you can read it at this link http://{settings.ALLOWED_HOSTS[0]}:{settings.ALLOWED_PORT}/posts/{instance.id}/ " \
                  f"you received this email because you are subscribed to this blog"
        send_mail(extendinguser.user.username,
                  message,
                  settings.PROJECT_EMAIL,
                  [extendinguser.user.email])
