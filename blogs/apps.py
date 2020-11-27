from django.apps import AppConfig


class BlogsConfig(AppConfig):
    name = 'blogs'

    def ready(self):
        from blogs import signals
