from django.contrib.auth.models import AbstractUser
from django.db import models

from tinymce.models import HTMLField


class User(AbstractUser):
    subscribed_to = models.ManyToManyField('Blog', blank=True)
    read_posts = models.ManyToManyField('Post', blank=True)

    def __str__(self):
        return self.username


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_blog',
                               null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return "{0}'s blog".format(self.author)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'User blog'
        verbose_name_plural = 'User blogs'


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)
    header = models.CharField(max_length=20, help_text="Enter a post header")
    text = HTMLField(help_text="Enter a post text")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return "{0} / {1}".format(self.blog, self.header)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
