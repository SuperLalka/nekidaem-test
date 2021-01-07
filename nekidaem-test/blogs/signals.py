from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from blogs.models import (
    Blog, Post, User
)
from nekidaem_test import settings


@receiver(post_save, sender=User)
def create_user_blog(instance, **kwargs):
    if not Blog.objects.filter(author=instance).exists():
        user_blog = Blog.objects.create(author=instance)
        user_blog.save()


@receiver(post_save, sender=Post)
def inform_the_subscriber(instance, **kwargs):
    list_of_subscriptions = list(User.objects.filter(
        subscribed_to=instance.blog))
    for user in list_of_subscriptions:
        message = f"Hello {user.user.username}, " \
                  f"a new post {instance.header} has appeared on the {instance.blog} blog, " \
                  f"you can read it at this link http://{settings.ALLOWED_HOSTS[0]}:{settings.ALLOWED_PORT}/posts/{instance.id}/ " \
                  f"you received this email because you are subscribed to this blog"
        send_mail(user.user.username,
                  message,
                  settings.PROJECT_EMAIL,
                  [user.user.email])
