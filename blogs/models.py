from django.conf import settings as django_settings
from django.db import models

from tinymce.models import HTMLField


class ExtendingUser(models.Model):
    user = models.OneToOneField(django_settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscribed_to = models.ManyToManyField('Blog')

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['user']
        verbose_name = 'Extra info | User'
        verbose_name_plural = 'Extra info | Users'


class Blog(models.Model):
    user = models.ForeignKey(ExtendingUser, on_delete=models.CASCADE, related_name='blog',
                             null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return "{0}'s blog".format(self.user)

    def check_author(self):
        pass

    class Meta:
        ordering = ['created_at']
        verbose_name = 'User blog'
        verbose_name_plural = 'User blogs'


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)
    header = models.CharField(max_length=20, help_text="Enter a post header")
    text = HTMLField(help_text="Enter a post text")
    read_by_user = models.ManyToManyField('ExtendingUser', editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return "{0} / {1}".format(self.blog, self.header)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

